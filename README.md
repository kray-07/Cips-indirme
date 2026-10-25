# 🎬 Video İndirici / Video Downloader

Bağlantı yapıştır, videoyu indir. [yt-dlp](https://github.com/yt-dlp/yt-dlp) ve Flask ile yapılmış basit, yerel bir web arayüzü.

*Paste a link, download the video. A simple local web UI built with Flask and yt-dlp.*

## ⚠️ Sorumluluk Reddi / Disclaimer

**TR:** Bu araç yalnızca indirme hakkına sahip olduğunuz içerikler (kendi videolarınız, lisansı uygun içerikler, izin verilen içerikler) için tasarlanmıştır. Telif hakkıyla korunan içeriği izinsiz indirmek ve birçok platformun kullanım şartlarını ihlal etmek yasa dışı olabilir. Aracın kullanımından doğan tüm sorumluluk kullanıcıya aittir. Geliştirici hiçbir sorumluluk kabul etmez.

**EN:** This tool is intended only for content you have the right to download (your own videos, properly licensed or permitted content). Downloading copyrighted material without permission may be illegal and may violate platforms' terms of service. The user is solely responsible for how they use it. The author accepts no liability.

## Özellikler / Features

- Birçok siteyi destekler (yt-dlp'nin desteklediği siteler)
- Kalite seçimi: en iyi, 720p, 480p, sadece ses (MP3)
- Tek dosya, kolay kurulum
- Sadece `127.0.0.1` üzerinde çalışır

## Kurulum / Installation

1. Python 3.9+ ve [ffmpeg](https://ffmpeg.org) kur.
2. Bağımlılıkları yükle:
   ```bash
   pip install -r requirements.txt
   ```
3. Çalıştır:
   ```bash
   python app.py
   ```
4. Tarayıcıda aç: http://localhost:5000

## Sorun Giderme / Troubleshooting

Bir site çalışmayı bırakırsa yt-dlp'yi güncelle:

```bash
pip install -U yt-dlp
```

Giriş gerektiren, DRM korumalı veya özel videolar indirilemez.

## 🔒 Güvenlik Notu / Security Note

Uygulama varsayılan olarak sadece yerel makineden erişilebilir. İnternete açmayı düşünüyorsan istek sınırı (rate limit), kimlik doğrulama ve kullanım limiti eklemelisin; aksi halde kötüye kullanılabilir.

## Lisans / License

[MIT](LICENSE)
