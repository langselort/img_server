namespace cpp img_service
namespace java img_service

struct GeneralResponse {
    1: i32 code,
    2: string msg,
    3: string data,
}

struct GeneralRequest {
    1: string img_file,
}

service ImgService {
  GeneralResponse upload_img (1: GeneralRequest request),
}
