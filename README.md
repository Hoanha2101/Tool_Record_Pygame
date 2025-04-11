# Hướng dẫn chạy RECORD TOOL

### Yêu cầu
+   python >= 3.8 (kiến nghị)
+   Kiểm tra python version

```bash
python --version
```


## Bước 1: Tạo môi trường ảo, kích hoạt môi trường ảo
```bash
python -m venv myenv
```
```bash
myenv\Scripts\activate
```

Folder map sẽ như sau:
```bash
|myenv/
|a_record.py
|README.md
|requirement.txt
```
## Bước 2: Cài đặt các thư viện
```bash
pip install -r requirement.txt
```
## Bước 3: CHẠY APP
```bash
python a_record.py
```
# Lưu ý:

Dòng `29`, file `a_record.py`
```python
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW) # mặc định camera của máy tính là 0.
```

+   Thay đổi số `0`, thành các số `1`, `2`, `3`, `4`,... tương ứng với id camera mà máy bắt được, để chọn đúng camera

+   Folder `collect_data`, sẽ tự sinh ra nếu chưa tạo.

```bash
collect_data/
    |---1.mp4
    |---2.mp4
    |---3.mp4
    |....
```
+ `1.mp4`, `2.mp4`, `3.mp4`, ... phát trong vscode không được, mở bên ngoài thư mục xem được thì data hợp lệ.


# Label 2 camera

```
collect_data/
├── top/
│   ├── left/
│   ├── right/
│   └── straight/
├── bottom/
|   ├── left/
|   ├── right/
|   └── straight/
└──video.mp4


```
Run code
```
python label2Camera.py
```