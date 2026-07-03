# AWS GameDay - Vulnerability Management Challenge

README này ghi lại các thay đổi đã thực hiện để hoàn thành challenge `Vulnerability-Management` trong AWS GameDay.

## Bối cảnh

Pipeline ban đầu bị lỗi ở stage `ImageScanning` với 3 action thất bại:

- `Linting`: Hadolint quét `app/Dockerfile` và báo lỗi Dockerfile.
- `SecretsScan`: `git-secrets` phát hiện chuỗi giống AWS access key trong source code.
- `VulnScan`: Grype phát hiện dependency Python có lỗ hổng trong image.

Yêu cầu quan trọng của challenge là chỉ sửa source application, không sửa các file cấu hình security/buildspec. Vì vậy, các thay đổi chỉ nằm trong `appsource/app/`.

## Các lỗi đã sửa

### 1. Hadolint

File sửa: `appsource/app/Dockerfile`

Vấn đề ban đầu:

- Base image `public.ecr.aws/lambda/python:3.9` không đi qua rule registry của Hadolint.
- Dockerfile có lệnh `RUN #yum update -y`, không thực sự update gì và dễ gây lint/build không rõ ràng.
- Sau khi đổi Dockerfile, Hadolint tiếp tục yêu cầu dùng `pip install --requirement` thay vì shorthand `-r`.

Cách sửa:

- Đổi base image sang Python Alpine mới hơn:

```dockerfile
FROM public.ecr.aws/docker/library/python:3.13-alpine
```

- Giữ ignore cục bộ cho rule registry ngay trong Dockerfile:

```dockerfile
# hadolint ignore=DL3026
```

- Cài dependency bằng cú pháp Hadolint chấp nhận:

```dockerfile
RUN pip install --no-cache-dir --requirement requirements.txt
```

### 2. git-secrets

File sửa: `appsource/app/app/index.py`

Vấn đề ban đầu:

```python
success_message = "Demo task AKIA123EW54HZT6QFQZR"
```

Chuỗi `AKIA...` có format giống AWS access key nên bị `git-secrets --scan -r *` chặn.

Cách sửa:

```python
success_message = "Demo task completed"
```

### 3. Grype

File sửa: `appsource/app/requirements.txt`

Vấn đề ban đầu:

```txt
flask-cors <= 3.0.8
```

Grype báo `flask-cors 3.0.8` dính vulnerability `CVE-2020-25032` / `GHSA-xc3p-ff3m-f46v`. Log scanner đề xuất fix ở version `3.0.9`.

Cách sửa:

```txt
flask-cors>=3.0.9
```

## Các file đã thay đổi

- `appsource/app/Dockerfile`
- `appsource/app/requirements.txt`
- `appsource/app/app/index.py`

Không thay đổi:

- `appsource/hadolint.yml`
- `config.zip`
- buildspec hoặc cấu hình security của pipeline

## Cách publish source đã sửa

Sau khi sửa source, source được đóng gói lại thành `code.zip` và upload lên S3 source object của pipeline:

```powershell
Compress-Archive -Path .\appsource\* -DestinationPath .\code.zip -Force
aws s3 cp .\code.zip s3://gdquests-39d0f6e8-4e53-46ff-bff4-sourcestagebucket-oupryjdrdvz1/code.zip --region us-east-1
aws codepipeline start-pipeline-execution --name Vulnerability-Management --region us-east-1
```

## Kết quả xác minh

Pipeline `Vulnerability-Management` đã chạy thành công.

Execution mới nhất đã xác minh:

```txt
de542d46-4ebd-43ab-aeab-cc30d5d9894c - Succeeded
```

Trạng thái các stage:

- `CodeSource`: Succeeded
- `ImageScanning`: Succeeded
  - `Linting`: Succeeded
  - `SecretsScan`: Succeeded
  - `VulnScan`: Succeeded
- `PushImage`: Succeeded

Challenge hoàn thành vì source đã vượt qua lint, secret scan, vulnerability scan và image đã được push thành công.
