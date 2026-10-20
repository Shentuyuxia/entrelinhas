/* Open-source neural voices (Piper) running on this device.
   espeak-ng phonemizer (WebAssembly) + ONNX Runtime Web. Text never leaves the device.
   Voice models come from huggingface.co/rhasspy/piper-voices and are kept in Cache Storage. */
const ROOT = new URL("../", self.location.href).href;
importScripts(ROOT + "vendor/ort/ort.wasm.min.js", ROOT + "vendor/piper/piper_phonemize.js");
ort.env.wasm.wasmPaths = ROOT + "vendor/ort/";
ort.env.wasm.numThreads = 1;            // GitHub Pages is not cross-origin isolated
ort.env.logLevel = "error";

const HF = "https://huggingface.co/rhasspy/piper-voices/resolve/main/";
const VOICE_CACHE = "piper-voices-v1", ASSET_CACHE = "piper-assets-v1";
const voiceUrl = id => { const [loc, name, q] = id.split("-"); return HF + loc.slice(0, 2) + "/" + loc + "/" + name + "/" + q + "/" + id + ".onnx"; };

async function cachedBuf(cacheName, url) {
  const c = await caches.open(cacheName);
  const hit = await c.match(url);
  if (hit) return hit.arrayBuffer();
  const res = await fetch(url);
  if (!res.ok) throw new Error("HTTP " + res.status + " " + url.split("/").pop());
  const buf = await res.arrayBuffer();
  try { await c.put(url, new Response(buf.slice(0))); } catch (e) {}
  return buf;
}

let PH = null; // {wasm, data}
async function phonemizerAssets() {
  if (!PH) PH = Promise.all([
    cachedBuf(ASSET_CACHE, ROOT + "vendor/piper/piper_phonemize.wasm"),
    cachedBuf(ASSET_CACHE, ROOT + "vendor/piper/piper_phonemize.data")
  ]).then(([wasm, data]) => ({ wasm, data })).catch(e => { PH = null; throw e; });
  return PH;
}
async function phonemize(texts, espeakVoice) {
  const { wasm, data } = await phonemizerAssets();
  const out = [];
  const m = await createPiperPhonemize({
    wasmBinary: wasm,
    getPreloadedPackage: () => data,
    print: l => { try { out.push(JSON.parse(l).phoneme_ids); } catch (e) {} },
    printErr: () => {},
    locateFile: f => ROOT + "vendor/piper/" + f
  });
  m.callMain(["-l", espeakVoice, "--input", JSON.stringify(texts.map(text => ({ text }))), "--espeak_data", "/espeak-ng-data"]);
  return out;
}

const SESS = new Map(); // id -> Promise<{s, cfg}>, keep at most two voices in memory
function session(id) {
  if (!SESS.has(id)) {
    const p = (async () => {
      const url = voiceUrl(id);
      const cfg = JSON.parse(new TextDecoder().decode(await cachedBuf(VOICE_CACHE, url + ".json")));
      const s = await ort.InferenceSession.create(new Uint8Array(await cachedBuf(VOICE_CACHE, url)), { executionProviders: ["wasm"] });
      return { s, cfg };
    })();
    p.catch(() => SESS.delete(id));
    SESS.set(id, p);
    while (SESS.size > 2) { const k = SESS.keys().next().value, old = SESS.get(k); SESS.delete(k); old.then(x => x.s.release && x.s.release()).catch(() => {}); }
  }
  return SESS.get(id);
}

async function synth(id, text, rate) {
  const { s, cfg } = await session(id);
  const [ids] = await phonemize([text], (cfg.espeak && cfg.espeak.voice) || id.slice(0, 2));
  if (!ids || !ids.length) return { pcm: new Float32Array(0), sr: cfg.audio.sample_rate };
  const inf = cfg.inference || {};
  const feeds = {
    input: new ort.Tensor("int64", BigInt64Array.from(ids.map(BigInt)), [1, ids.length]),
    input_lengths: new ort.Tensor("int64", BigInt64Array.from([BigInt(ids.length)]), [1]),
    scales: new ort.Tensor("float32", Float32Array.from([inf.noise_scale ?? 0.667, (inf.length_scale ?? 1) / (rate || 1), inf.noise_w ?? 0.8]), [3])
  };
  if (cfg.speaker_id_map && Object.keys(cfg.speaker_id_map).length) feeds.sid = new ort.Tensor("int64", BigInt64Array.from([0n]), [1]);
  const r = await s.run(feeds);
  const pcm = Float32Array.from(r.output.data);
  return { pcm, sr: cfg.audio.sample_rate };
}

self.onmessage = async e => {
  const { id, op } = e.data || {};
  try {
    if (op === "warm") { await Promise.all([phonemizerAssets(), session(e.data.voice)]); self.postMessage({ id, ok: true }); }
    else if (op === "synth") { const r = await synth(e.data.voice, e.data.text, e.data.rate); self.postMessage({ id, ok: true, pcm: r.pcm, sr: r.sr }, [r.pcm.buffer]); }
    else if (op === "drop") { SESS.delete(e.data.voice); self.postMessage({ id, ok: true }); }
  } catch (err) {
    self.postMessage({ id, ok: false, error: String(err && err.message || err) });
  }
};
