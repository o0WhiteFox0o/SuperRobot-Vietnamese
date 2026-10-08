> **Ngôn ngữ / Language:** [Tiếng Việt](script-semantics-confirmation.vi.md) · [English](script-semantics-confirmation.en.md) · [中文](script-semantics-confirmation.md)

# Xác nhận ngữ nghĩa của các hướng dẫn còn lại

2026-09-12. Hiện tại, 1.812 sự kiện có thể được phân tích cú pháp đến bộ kết thúc, đồng thời bao gồm các ranh giới và bảng phân phối của 73 vị trí của lệnh thông thường và 30 loại lệnh có điều kiện. Thẻ ngữ nghĩa của hướng dẫn thông thường là: 73 mục `code-confirmed`, 0 mục `structure-confirmed`, 0 mục `unknown` (2026-09-17, sau lần kiểm tra cấp độ nhỏ lần lượt). Ba trạng thái này ghi lại sức mạnh của bằng chứng và `code-confirmed` không bằng việc hoàn thành chấp nhận vận hành trò chơi.

Mục đích là để xác nhận ý nghĩa tham số, thay đổi trạng thái, điều kiện hoàn thành không đồng bộ và hiệu ứng trò chơi cho các lệnh còn lại, sau đó quyết định những lệnh nào an toàn để sử dụng trong các mod cấp độ. Ở giai đoạn này, chúng tôi không ghi lại ROM gốc cũng như không sử dụng trình xem cốt truyện làm trình thông dịch tập lệnh.

Hai lần chạy im lặng đã kiểm tra tất cả 123 lần mở siêu kiểu nữ và tất cả 56 lệnh thông thường/đối thoại cho các lần mở siêu kiểu nam. Đối với phần trước, hãy xem [Quan sát lần chạy đầu tiên](script-runtime-observation.md); đối với trường hợp sau, hãy xác nhận rằng tham số đầu tiên của `3D3C` là số trình điều khiển. Năm chuyển động tham số ban đầu có mã và khung liên tục hỗ trợ lẫn nhau. Xem [Quan sát hoạt động 3D3C](script-3d3c-runtime.md). Các ranh giới như vị trí tương đối và tọa độ logic vẫn cần những thí nghiệm đặc biệt.

Bước thứ hai vào ngày 16-09-2026 là [Cấp nhỏ](mini-stage.md): Việc tiêm chỉ có thể được thực hiện khi bản đồ chiến thuật không hoạt động và không thể tiếp cận lớp phủ bản đồ thế giới, cũng như không thể sắp xếp đội hình tấn công mà bạn cần. Các cấp độ tự tạo có thể cung cấp cả hai, do đó, người ta xác nhận rằng `3D32` (định vị bản đồ thế giới, độ dài cố định 106 VI), `3D33` (bản đồ thế giới di chuyển, vẽ đường đi, phát triển theo khoảng cách), `3D31` (cùng chức năng xử lý như `3D32`, hoạt động giống nhau), `3D50` (biến dạng cơ thể, thay đổi số phiên bản cơ thể, HP và tọa độ được giữ lại), `3D58` (chuyển trại, các vị trí trong danh sách di chuyển qua các bên), `3D5C` (hợp nhất/tách, danh sách tăng thêm bốn vị trí sau khi tách), `3D6E` (đơn vị thoát ra). Vòng đấu tương tự cũng loại bỏ một số hiểu lầm: `3D68` thuộc về lớp phủ chiến thuật chứ không phải bản đồ thế giới; `3D70`/`3D6F`/`3D69` là no-op thay vì không có tác dụng khi mục tiêu không tồn tại; `3D49` gặp sự cố khi được kích hoạt và vẫn giữ nguyên `unknown`.

Bắt đầu từ ngày 16 tháng 9 năm 2026, bạn có thể sử dụng [gỡ lỗi chèn tập lệnh](script-debug-injection.md) để chuyển hướng dẫn tùy chỉnh cho công cụ ban đầu để thực thi: đợt xác nhận chạy đầu tiên `3D3B` bốn loại mờ dần và mờ dần, `3D38` 2 VI mỗi lần đếm, `3D35` cuộn không chặn, `3D34` Trên thực tế, đó là để chuyển đổi bản đồ (tham số đầu tiên là số bản đồ), `3D45` xuất hiện, `3D46` thoát ra, `3D3C` chuyển động tuyệt đối, `3D5B` tiền, `3D6C` phần chuyển đổi, `3D5F` sức mạnh tổng thể −30, `3E13/3E03/3E1D` Cuộc trò chuyện với các quy trình nhánh và điểm đánh dấu tuyến đường, `3D3E/3D3F`. Kết quả được ghi vào trường `runtime` của mỗi lệnh của khóa bố cục.

## Quá trình xác nhận cho mỗi lệnh

1. **Chọn mẫu và sửa bằng chứng. ** Tìm tất cả các vị trí xuất hiện của lệnh từ thư mục và đăng ký ROM SHA, cảnh, địa chỉ sự kiện, độ lệch lệnh, tham số ban đầu, lệnh trước và tiếp theo cũng như điều kiện nhánh. Ưu tiên cho hai trường hợp dễ tái tạo và có giá trị tham số tương phản; các lệnh không sử dụng trong tập lệnh gốc sẽ được đánh dấu riêng.
2. ** Bắt kịp lớp dưới cùng để đọc và viết. ** Nhập lớp phủ chính xác từ trình xử lý thường trú để theo dõi các máy trạng thái, mức tiêu thụ tham số, đọc và ghi các mục trong bảng, bảng phân công hoặc trường công cụ cũng như các chức năng tiếp theo sử dụng các trường này. Hàm xử lý có thể được gọi nhiều lần trên mỗi khung. Cần phải phân biệt giữa lần nhập đầu tiên, chờ đợi và hoàn thành, đồng thời kiểm tra thời gian tiến hành tập lệnh của PC. Các tham số giữ chỗ chưa đọc vẫn được giữ lại và không thể xóa nếu không được phép.
3. **Theo dõi hoạt động im lặng. ** Thêm một dấu vết định hướng có thể đóng trong bản recomp gốc để ghi lại việc bắt đầu/hoàn thành lệnh, số khung, cảnh, PC sự kiện, dấu nhân vật chính, ACC điều kiện, các biến liên quan và trạng thái đơn vị trước và sau các giá trị. Chỉ lọc các sự kiện hoặc lệnh được nhắm mục tiêu để tránh làm ngập bằng chứng trong từng khung đầu ra. Sử dụng các hiệu ứng căn chỉnh màn hình hoặc video để xác nhận rằng việc hoàn thành hướng dẫn thực sự tương ứng với những thay đổi được quan sát.
4. **Thí nghiệm kiểm soát một tham số. ** Trong cấu hình thử nghiệm độc lập, bản sao lưu trữ và lớp phủ bộ nhớ tạm thời, hãy so sánh giá trị ban đầu với giá trị đã thay đổi; trước tiên hãy xác minh rằng đường cơ sở có thể được lặp lại trước khi thay đổi một yếu tố. Khái quát hóa kết luận trước khi có ít nhất hai bối cảnh ban đầu khớp nhau; kiểm tra sau biểu diễn các đơn vị, trại, tọa độ, lượt, tình trạng lưu trữ. Kết thúc và khôi phục cài đặt gốc và quá trình chạy thử sẽ vẫn ở chế độ im lặng.
5. **Chèn lấp và kiểm tra lại. ** Cập nhật tên tham số, ngữ nghĩa và cửa sổ bằng chứng trong khóa bố cục, thêm thử nghiệm phiên bản thực, sắp xếp lại byte thô và kiểm tra ranh giới, đồng thời trích xuất lại thư mục. Các kết luận tĩnh, quan sát hoạt động, phản ví dụ và các bit không giải thích được lần lượt được lưu trong bản ghi bằng chứng và trạng thái ngữ nghĩa chỉ được nâng cấp khi bằng chứng hỗ trợ nó.

Bạn nên ghi lại từng mục một cách độc lập: `opcode / handler / overlay / source occurrences / parameter hypotheses / code evidence / runtime trace / changed parameter / observed effect / confidence / unresolved`. Bản ghi đang chạy phải bao gồm ROM, phiên bản xây dựng, mục kiểm tra và cài đặt tắt tiếng; bạn không thể chỉ viết "trông giống như một vụ nổ".

## Ưu tiên vòng 1

Thời gian trong bảng bên dưới được lấy từ thống kê lệnh sự kiện độc lập hiện tại của ROM gốc và các kịch bản chia sẻ không được tích lũy nhiều lần. Tiêu đề là mô tả về công nghệ hiện có và không thể xác định trước hiệu quả hoàn chỉnh dựa trên nó.

| Trình tự | Lệnh | Số lần xuất hiện | Những điểm chính cần được xác nhận |
| --- | --- | ---: | --- |
| 1 | `3D3C` | 486 | Di chuyển theo đơn vị do người lái xe chỉ định: Năm ví dụ về quan sát và so sánh tham số đơn mục tiêu tuyệt đối đã được hoàn thành, vị trí tương đối và các ranh giới khác vẫn chưa được chấp nhận |
| 1 | `3D36` | 196 | Hiệu suất Bản đồ/Bản đồ Thế giới: Ý nghĩa của byte thấp, các nhánh máy trạng thái |
| 1 | `3D55` | 169 | Hiệu suất đơn vị: phân tích tham số ký tự và hiệu ứng tham số thứ hai |
| 2 | `3D32` / `3D33` | 661/166 | Mối tương quan giữa cánh đồng, con người và địa điểm trong bảng bản đồ thế giới `801C5310` |
| 2 | `3D6B` / `3D69` | 59/28 | Hoạt động vai trò và byte trạng thái: trường danh sách nào bị ảnh hưởng và liệu chúng có thể được duy trì hay không |
| 2 | `3D6E` / `3D6F` / `3D70` | 53/30/13 | Các thao tác trên bảng vai trò và liên kết, xác nhận ai sẽ tiêu thụ sau khi viết |
| 3 | `3D49` / `3D67` / `3D58` / `3D5C` | 30/23/18/12 | Hiển thị các mục, số đặc biệt, liên kết BGM và các thông số biến thể |
| 3 | `3D75` / `3D50` / `3D5E` / `3D63` / `3D68` | 9/4/3/1/1 | Các phiên bản tần số thấp lần lượt thiết lập các lối vào thử nghiệm có thể lặp lại |
| Cuối cùng | `3D31` | 0 | Trình xử lý được chia sẻ với `3D32`; theo dõi tĩnh được ưu tiên, các thí nghiệm xây dựng nhân tạo không thể chứng minh rằng trò chơi gốc sử dụng nó |

`3D3C` Đã hoàn thành [Kiểm soát cách ly](script-3d3c-experiment.md) vị trí mục tiêu của Brad `1912 → 1911`: Trong cùng một hệ nhị phân, tọa độ logic của điểm cuối và danh sách yêu tinh được di chuyển lên một khoảng trắng, lệnh mở tiếp theo đã được hoàn thành và các tham số đã được khôi phục. Tiếp theo, xác nhận các ranh giới như vị trí tương đối, nhiều đơn vị có cùng số lượng và các mục tiêu bị thiếu, sau đó nâng cao các lệnh thực hiện khác của cùng một lớp phủ. Các khối hiện được liệt kê theo danh sách hợp lệ và các quy tắc va chạm và đi qua vẫn chưa được chấp nhận.

## Các mục còn lại quan trọng hơn để chỉnh sửa cấp độ

- Ý nghĩa của ~~`3E06/3E0D` trường danh sách `+5`, `+0x14`~~: 2026-10-01 Mã được xác nhận là cấp độ và số lần tiêu diệt, xem [Thành phần ẩn](../gameplay/hidden-elements.md) Phần 2.4.
- ~~Người viết `+0x992` thuộc loại 9~~: 2026-10-01 được xác nhận là cư dân `800A4634`; tiêu đề là [người thuyết phục, đối tượng, biến ngưỡng, giá trị ngưỡng], ngưỡng là điều kiện tiên quyết của mỗi bước thuyết phục, xem [Thành phần ẩn](../gameplay/hidden-elements.md) Mục 3.
- `3E16/3E17/3E19/3E1A`: Nguồn và ý nghĩa điều kiện của trường ký tự chiến tranh và động cơ (`3E18` đã được xác nhận đọc chỉ mục cảnh hiện tại), trước tiên hãy kiểm tra người viết, sau đó so sánh trình kích hoạt sự kiện.
- Loại 13: Đường dẫn chính xác vào trạng thái cấu hình ban đầu `engine+4 = 0xC2`.
- Bản ghi sắp xếp 28 byte: các trường không được giải thích như `+8`, `+E`–`+13`, `+1A` và 13 khối không có dấu kết thúc 999 được căn chỉnh. Các trường đoán hoặc dấu kết thúc có thể không được thêm vào để tạo điều kiện chỉnh sửa.
- Số còn lại trong tiêu đề văn bản, loa tương đối của phân đoạn chung và `3D4B 500` khôi phục nguồn thời gian chạy của cảnh.

Các mục này xác định độ tin cậy của việc phát lại tuyến đường và các bản sửa đổi và phải được lên lịch ở cùng cấp độ với thứ tự hiển thị. Phân tích tĩnh đã có thể hỗ trợ việc đọc toàn văn; tự động gấp tuyến đường thực yêu cầu ngữ nghĩa có điều kiện và trạng thái đang chạy ở trên, đồng thời việc ghi lại tập lệnh cũng yêu cầu các chuyến đi khứ hồi byte độc ​​lập và chấp nhận trò chơi.

Để biết mối quan hệ giữa mã nhập và mã máy, hãy xem [Phân tích hoàn chỉnh các tập lệnh cấp độ](stage-script-exploration.md); để biết các khả năng của phía đọc, hãy xem [Trạm đánh giá lô](story-reader.md).


## Danh sách đầy đủ về ngữ nghĩa hiện chưa rõ và lộ trình phân tích mã C

16-09-2026 Kiểm tra: Giải mã cấu trúc không có hướng dẫn về độ dài không xác định. Sau nhiều vòng xác minh cấp độ nhỏ, không có `unknown` cho các lệnh thông thường (hai lệnh cuối cùng `3D75` và `3D63` đã được hoàn tất vào ngày 17-09-2026: lệnh trước phát hành các thiết bị do tàu mẹ mang theo và lệnh sau chuyển đổi giữa hạ cánh/bay, xem [Cấp nhỏ](mini-stage.md)).

Mười ba lượt xem [Cấp độ nhỏ](mini-stage.md) được nâng cấp lên `code-confirmed` trong vòng này: Ngoài ra còn có `3D55` của vòng thứ tư - tham số thứ hai của nó là số lệnh tinh thần sau khi so sánh** (chỉ có 11 giá trị được sử dụng ở mức 169 trong tập lệnh gốc, ngoại trừ Sentinel 30. Tất cả các trường hợp ngoại lệ đều tương ứng với tinh thần thực sự: tăng tốc/nồng độ/ひらめき/bản chất gốc/phải đánh/tường sắt/máu nóng/気合/ドbản chất gốc/linh hồn; bảng byte `80217D20` là dữ liệu không hợp lệ sau đúng 31 mục, giá trị bảng 15/1 là loại mục tiêu) và màn hình kích hoạt là viên kim cương phát sáng. Ngoài ra, vòng đầu tiên `3D31`/`3D32`/`3D33`/`3D50`/`3D58`/`3D5C`/`3D6E`; vòng thứ hai `3D49` (hiệu suất chiến đấu theo kịch bản), `3D6F` (xóa bit cờ thành phần) 2), `3D70` (được gắn với các ký tự đi cùng hành khách); `3D67` (bật vòng âm thanh thứ ba) (hiệu suất cắt, mỗi giá trị trong bốn giá trị là một máy đi qua đường hầm tốc độ ánh sáng, tương quan mức lấy mẫu chỉ +0,007, chứng tỏ âm thanh khác nhau) và `3D68` (máy ảnh kéo về đơn vị đã chọn, so sánh từng khung hình được hoàn tất và xác nhận là im lặng). `3D55` đã được nâng cấp từ `unknown` lên `structure-confirmed`: Đã xác nhận rằng nó sẽ di chuyển máy ảnh và chọn thiết bị. Tham số thứ hai được liệt kê trong bảng `80217D20` và các hiệu ứng đặc biệt của đơn vị được thêm vào (9 là một viên kim cương phát sáng). Sự tương ứng từng mục vẫn chưa được hoàn thành.

Phương pháp hữu ích nhất trong vòng này: **0 "no-op" của VI hầu như đều bị thiếu đối tượng, thay vì các hướng dẫn không hợp lệ. ** `3D6F` Thay thế bằng số thực sự tồn tại trong bảng phần liên quan và kết quả sẽ xuất hiện; `3D70` Theo phương pháp viết tập lệnh gốc, trước tiên hãy sử dụng `3D5A` để đăng ký ký tự đồng hành khách vào bảng điều khiển và kết quả sẽ xuất hiện; `3D49` thậm chí còn triển khai hai ký tự trên bản đồ và sự cố sẽ chuyển thành hoạt động bình thường. Một số khác (`3D58 59,0`, `3D69 4,1`) thực sự là bình thường - trạng thái mục tiêu đã được thiết lập.

Bước phiên bản trình điều khiển là 0x4C, phiên bản khung máy bay là 0x54 và vị trí danh sách là 0x14, tất cả đều xuất phát từ sự khác biệt từng byte giữa vòng này và vòng tiêm-2.

Lệnh có điều kiện không có `unknown` nhưng sáu mục `3E06 / 3E0D / 3E16 / 3E17 / 3E19 / 3E1A` vẫn là `structure-confirmed`: mã để so sánh hoặc gán đã được biết và ý nghĩa, nguồn gốc hoặc trường hợp đặc biệt của trò chơi của các trường liên quan vẫn chưa được xác nhận đầy đủ. Không có phiên bản `3E19 / 3E1A` nào trong tập lệnh gốc.

### Bạn có thể trực tiếp sử dụng phân tích C được tạo

Thư mục được tạo `build/recomp/cpu-bound/generated/` giữ lại các chức năng xử lý hoàn chỉnh và chú thích địa chỉ MIPS, đồng thời có thể theo dõi trực tiếp các mối quan hệ đọc, ghi và gọi. Đây là bản recomp cấp độ đăng ký C. Common `ctx->rN`, `MEM_W/MEM_H/MEM_BU`, `LOOKUP_FUNC` không có tên biến và loại cấu trúc của nhà phát triển ban đầu; nó phải tương ứng với ROM gốc và khóa thế hệ, đồng thời không được sửa đổi các tệp được tạo này. Cùng một VRAM có thể tương ứng với các chức năng khác nhau trong các lớp phủ khác nhau và phải được phân biệt bằng cách sử dụng các tiền tố như `resident` / `load_000AB160` / `load_000A7EC0`.

Vòng kiểm tra tại chỗ này đã tìm ra manh mối rõ ràng có thể được khám phá thêm, nhưng không có nâng cấp hàng loạt trạng thái ngữ nghĩa dựa trên điều này:

- **3D69**: Tham số thứ hai của `load_000AB160_func_802128E4` lấy byte thấp, giá trị 0 sẽ xóa trình điều khiển `+0x35`, giá trị khác 0 sao chép `+0x34` sang `+0x35`; cũng tìm kiếm thiết bị điều khiển, xử lý các trình điều khiển khác và gọi `801F94D0`. Nó không phải là một giá trị tùy ý được ghi trực tiếp vào byte trạng thái. Bước tiếp theo là thực hiện khởi tạo hai trường, cập nhật vòng và trình đơn để xác nhận tên trò chơi của nó.
- **3D6F**: `resident_func_800ACF44` quét 700 bản ghi 36 byte, kiểm tra byte hợp lệ, khớp với số `+2`, sau đó xóa bit `0x04` của bản ghi trùng khớp đầu tiên `+0x22`. Trọng tâm còn lại là bộ thiết lập và đầu đọc bit; điều này chủ yếu được thúc đẩy bởi các tham chiếu chéo tĩnh.
- **3D55**: `load_000AB160_func_80210490` không chỉ kiểm tra phi công chính mà còn duyệt qua các con trỏ của người lái bắt đầu từ `+0x38` theo số lượng máy bay `+0x34`. Sau khi tìm thấy nó, hãy đặt sprite và ống kính đã chọn. Tham số thứ hai tiếp tục đi vào các bảng `80217D20` và `801D6A68`, các bảng này phải được phân tích dọc theo dòng xuống. Bạn không thể đoán được hiệu quả hoạt động chỉ bằng cách sử dụng tên mục nhập.
- **3D5E**: `load_000A7EC0_func_801C517C` chỉ có 14 hướng dẫn với các địa chỉ khác nhau, cài đặt `801C58C4=2`, gọi `80080188(6)` và `80099814(5,1,2)`. Chức năng ngắn gọn không có nghĩa là ngữ nghĩa của trò chơi đã hoàn chỉnh. Bước tiếp theo là phân tích cú pháp người tiêu dùng của trường trạng thái.

Phần tiếp theo chủ yếu là phân tích tĩnh C: quy trình đầu tiên `3D69/3D6B/3D6E/3D6F/3D70` và các trường cấu trúc của sáu lệnh điều kiện trên; sau đó theo đuổi các máy trạng thái tần số cao như `3D36/3D55`. Đăng ký trực tiếp bằng chứng mã với ngữ nghĩa được xác nhận bởi chuỗi đọc-ghi hoàn chỉnh; chạy im lặng để kiểm tra hình ảnh, thời gian, các nhánh đặc biệt và khả năng tương thích viết lại. Không cần phải chạy đi chạy lại toàn bộ phần mở đầu cho mỗi lệnh gán thông thường.