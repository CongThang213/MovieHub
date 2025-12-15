# MovieHub API

## Giới thiệu
MovieHub API là phần Backend (Server-side) cho hệ thống đặt vé xem phim trực tuyến. Dự án này cung cấp các RESTful API để quản lý dữ liệu rạp chiếu, phim, và xử lý logic đặt chỗ ngồi.

Hiện tại, dự án tập trung hoàn thiện lớp xử lý dữ liệu và API, sẵn sàng để tích hợp với các nền tảng Frontend (Web hoặc Mobile).

## Chức năng chính (Backend)
- **Quản lý Phim:** API CRUD (Thêm, Xem, Sửa, Xóa) thông tin phim.
- **Quản lý Lịch chiếu:** Xử lý thời gian và phòng chiếu.
- **Hệ thống Ghế:** Quản lý sơ đồ ghế và trạng thái ghế (trống/đã đặt).
- **Đặt vé:** API xử lý giao dịch đặt vé.

## Công nghệ sử dụng
- **Ngôn ngữ:** Python
- **Kiến trúc:** RESTful API

## Trạng thái
**Backend Only:** Dự án hiện bao gồm mã nguồn Backend và API. Chưa bao gồm giao diện người dùng.

## Cài đặt
  ** Chạy server cục bộ
  uvicorn main:app --reload
