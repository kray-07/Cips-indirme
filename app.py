"""
Video İndirici - Flask + yt-dlp
Kurulum:
    pip install flask yt-dlp
    (ffmpeg kurulu olmalı: https://ffmpeg.org)
Çalıştırma:
    python app.py
Sonra tarayıcıda: http://localhost:5000

Not: Yalnızca indirme hakkına sahip olduğunuz içerikleri indirin.
Birçok platformun kullanım şartları indirmeyi yasaklar.
"""
import os
import shutil
import tempfile

from flask import Flask, after_this_request, jsonify, request, send_file
import yt_dlp

app = Flask(__name__)

HTML = """<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Video İndirici</title>
<style>
  body{font-family:system-ui,sans-serif;background:#0f172a;color:#e2e8f0;
       display:flex;justify-content:center;padding:24px}
  .card{max-width:520px;width:100%;background:#1e293b;padding:24px;border-radius:16px}
  h1{margin:0 0 16px;font-size:22px}
  input,select,button{width:100%;padding:12px;border-radius:10px;border:0;
       font-size:16px;margin-top:10px;box-sizing:border-box}
  input,select{background:#0f172a;color:#e2e8f0;border:1px solid #334155}
  button{background:#3b82f6;color:#fff;font-weight:600;cursor:pointer}
  button:disabled{opacity:.5}
  #info{margin-top:14px;font-size:14px;color:#94a3b8}
  #err{color:#f87171;margin-top:10px;font-size:14px}
</style>
</head>
<body>
<div class="card">
  <h1>🎬 Video İndirici</h1>
  <input id="url" type="url" placeholder="Video bağlantısını yapıştır…">
  <button id="check">Kontrol et</button>
  <div id="info"></div>
  <select id="fmt" style="display:none">
    <option value="best">En iyi kalite (MP4)</option>
    <option value="720">720p</option>
    <option value="480">480p</option>
    <option value="audio">Sadece ses (MP3)</option>
  </select>
  <button id="dl" style="display:none">İndir</button>
  <div id="err"></div>
</div>
<script>
const $ = id => document.getElementById(id);
$('check').onclick = async () => {
  $('err').textContent = ''; $('info').textContent = 'Kontrol ediliyor…';
  $('dl').style.display = $('fmt').style.display = 'none';
  try {
    const r = await fetch('/api/info', {method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({url: $('url').value.trim()})});
    const d = await r.json();
    if (!r.ok) throw new Error(d.error);
    $('info').textContent = d.title + (d.duration ? ' (' + Math.round(d.duration/60) + ' dk)' : '');
    $('dl').style.display = $('fmt').style.display = 'block';
  } catch (e) { $('info').textContent = ''; $('err').textContent = e.message; }
};
$('dl').onclick = () => {
  const q = new URLSearchParams({url: $('url').value.trim(), fmt: $('fmt').value});
  window.location = '/api/download?' + q;
};
</script>
</body>
</html>"""


def format_selector(fmt):
    if fmt == "audio":
        return {"format": "bestaudio/best",
                "postprocessors": [{"key": "FFmpegExtractAudio",
                                    "preferredcodec": "mp3"}]}
    if fmt in ("720", "480"):
        return {"format": f"bestvideo[height<={fmt}]+bestaudio/best[height<={fmt}]",
                "merge_output_format": "mp4"}
    return {"format": "bestvideo+bestaudio/best", "merge_output_format": "mp4"}


@app.get("/")
def index():
    return HTML


@app.post("/api/info")
def info():
    url = (request.get_json(silent=True) or {}).get("url", "")
    if not url.startswith(("http://", "https://")):
        return jsonify(error="Geçerli bir bağlantı gir."), 400
    try:
        with yt_dlp.YoutubeDL({"quiet": True, "noplaylist": True}) as ydl:
            d = ydl.extract_info(url, download=False)
        return jsonify(title=d.get("title", "Video"), duration=d.get("duration"))
    except Exception:
        return jsonify(error="Bu bağlantıdan video bulunamadı."), 400


@app.get("/api/download")
def download():
    url = request.args.get("url", "")
    fmt = request.args.get("fmt", "best")
    if not url.startswith(("http://", "https://")):
        return "Geçersiz bağlantı", 400

    tmp = tempfile.mkdtemp()
    opts = {"quiet": True, "noplaylist": True,
            "outtmpl": os.path.join(tmp, "%(title).80s.%(ext)s"),
            **format_selector(fmt)}
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
        path = os.path.join(tmp, os.listdir(tmp)[0])
    except Exception:
        shutil.rmtree(tmp, ignore_errors=True)
        return "İndirme başarısız oldu.", 500

    @after_this_request
    def cleanup(resp):
        shutil.rmtree(tmp, ignore_errors=True)
        return resp

    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
