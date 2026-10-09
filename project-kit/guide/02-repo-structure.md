# 02 — Cấu trúc repository chuẩn

Rút ra từ SuperRobot, đã tổng quát hoá. Nguyên tắc: **mỗi thư mục có một trách nhiệm; thứ sinh ra được thì không commit; thứ không phân phối được thì khoá bằng hash.**

```text
<project>/
├─ README.md                  # Tổng quan + đường vào nhanh (có thanh ngôn ngữ nếu đa ngữ)
├─ CONTRIBUTING.md            # Quy ước đóng góp, cách chạy test, quy tắc tài liệu
├─ LICENSE
├─ Makefile / justfile        # MỘT lệnh dựng từ clone mới đến chạy được
├─ pyproject.toml / package.json / CMakeLists.txt
├─ requirements.lock          # Khoá phụ thuộc (tái lập được)
├─ .editorconfig  .gitattributes  .gitignore
│
├─ src/                       # Mã nguồn sản phẩm, chia module theo trách nhiệm
│   ├─ core/                  #   Logic miền độc lập nền tảng (không I/O)
│   ├─ adapter/               #   Nối với hệ thống gốc / dịch vụ ngoài
│   ├─ ui/ | presentation/    #   Giao diện / trình bày
│   └─ platform/              #   Phần phụ thuộc OS (tách rõ từng nền tảng)
├─ tools/                     # Script phát triển, chia thư mục con theo MỤC ĐÍCH
│   ├─ toolchain/             #   Dựng, sinh mã, chuẩn bị phụ thuộc
│   ├─ run/                   #   Khởi chạy, điều khiển
│   ├─ verify/                #   Kiểm chứng có giới hạn (bounded verification)
│   ├─ analysis/              #   Phân tích offline
│   └─ debug/                 #   Giao diện gỡ lỗi / CLI / MCP
├─ tests/                     # Test tự động (đơn vị, thành phần, tài liệu)
├─ config/                    # Cấu hình dựng/chạy (profile, input script, định nghĩa)
├─ content/                   # Nội dung/dữ liệu do dự án quản lý (có lược đồ)
├─ reference/                 # Tài liệu/dữ liệu tham khảo được phép lưu (kèm hash)
├─ assets/                    # Sản phẩm sinh ra lớn, KHÔNG commit (README.md giải thích)
├─ build/                     # Bằng chứng chạy cục bộ, KHÔNG commit
├─ dist/                      # Gói phát hành, KHÔNG commit
├─ scripts/                   # Điểm vào cho người dùng cuối (double-click / launcher)
├─ cmake/ | build-support/    # Mô-đun dựng
├─ web/                       # Trang giới thiệu/tải xuống (nếu có)
├─ .github/workflows/         # CI: test, test_docs, dựng gói
└─ docs/                      # Xem 03-doc-system.md
    ├─ README.md              #   Chỉ mục trung tâm (BẮT BUỘC liệt kê mọi doc)
    ├─ guide/  design/  analysis/  features/  quality/  decisions/
    └─ templates/             #   (tuỳ chọn) bản sao mẫu để chép khi viết doc mới
```

## Quy tắc đặt tên & ranh giới

| Quy tắc | Lý do |
| --- | --- |
| Thư mục `tools/` chia theo **mục đích** (toolchain/run/verify/analysis/debug), không theo người viết | Người mới tìm đúng công cụ; Python gói con import chéo gọn (`from pkg.verify import …`) |
| Phụ thuộc nền tảng gom vào `src/platform/<os>` | Port sang nền tảng mới không phải lục toàn bộ mã |
| `config/` chỉ chứa cấu hình; dữ liệu lớn ở `assets/`/`content/` | Review diff dễ, repo nhẹ |
| `build/` & `assets/` không commit nhưng **doc được phép trỏ tới** làm "bằng chứng cục bộ" | Giữ đường dẫn bằng chứng mà không phình repo |
| Một điểm vào dựng duy nhất (`make`) | Tái lập từ clone mới; CI dùng đúng lệnh đó |
| Mọi script ghi file chỉ định `encoding="utf-8"`, `newline="\n"` | Tránh khác biệt giữa Windows/macOS/Linux |

> [!TIP]
> Khi kiến trúc đổi, **di chuyển + cập nhật docs + test_docs xanh trong cùng một commit**. SuperRobot từng chuyển `tools/recomp/native-host` → `src/host` và chia lại `tools/recomp/` theo mục đích theo cách này.

