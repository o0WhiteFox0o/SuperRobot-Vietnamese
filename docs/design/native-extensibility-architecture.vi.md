> **Ngôn ngữ / Language:** [Tiếng Việt](native-extensibility-architecture.vi.md) · [English](native-extensibility-architecture.en.md) · [中文](native-extensibility-architecture.md)

# Khuyến nghị về Kiến trúc Mod Nội dung và Đa ngôn ngữ SRW64

12-09-2026: Giai đoạn sản phẩm, cài đặt mặc định, lưu nút an toàn và chấp nhận chất lượng ngôn ngữ/hình ảnh để
[Lộ trình MOD tích hợp](mod-roadmap.md) sẽ được áp dụng. Hiện tại, chúng tôi chỉ tổ chức các chức năng của riêng mình thành các mô-đun MOD và biên dịch chúng trực tiếp vào máy chủ; chúng tôi không kết nối với các MOD bên ngoài. Giao diện ngữ nghĩa, phân lớp nội dung và lưu ranh giới của bài viết này có thể được sử dụng lại; tải gói bên ngoài, quyền truy cập `.nrm`, phân phối cộng đồng và SDK công khai thuộc về nghiên cứu kiến ​​trúc bị đình chỉ và không phải là nhiệm vụ hoặc công cụ chặn hiện tại.

Ngày: 2026-09-10; Cập nhật trạng thái thực hiện: 2026-09-11. Đợt tái cấu trúc đầu tiên đã bắt đầu: đường cơ sở chạy JP thống nhất, thư mục ngôn ngữ độc lập, gói nghệ thuật thuần túy và chuyển đổi hình ảnh/HD gốc trong khi chạy. Xem [Triển khai lần đầu](../native/native-content-foundation.md) để biết chi tiết. Các chương còn lại tiếp tục là kiến ​​trúc mục tiêu và không có nghĩa là SDK đã được phát hành.

Mục tiêu là hỗ trợ tiếng Nhật và tiếng Trung gốc trong cùng một chương trình bản địa, cho phép những người đóng góp khác thêm gói ngôn ngữ và dần dần hỗ trợ máy bay, nhân vật, vũ khí, tài nguyên và Mod cấp độ. Bài viết này phân biệt giữa các khả năng hiện có và các giao diện được đề xuất; đường dẫn mẫu, không gian tên và định dạng dữ liệu chưa có sẵn trong SDK.

## 1. Quyết định cốt lõi

1. Sử dụng ROM gốc tiếng Nhật bị khóa làm đường cơ sở chạy thống nhất. Ngôn ngữ, tài nguyên HD, thay thế mô hình và Mod trò chơi được chọn riêng; cùng một cấu hình trò chơi có thể sử dụng các ngôn ngữ hiển thị khác nhau.
2. Tách biệt ID đối tượng trò chơi, tên hiển thị và vị trí tài nguyên. Dịch tên không thay đổi nhận dạng đơn vị và thay thế hình đại diện không thay đổi dữ liệu trình điều khiển.
3. Sử dụng gói dữ liệu cho ngôn ngữ, nghệ thuật chung và sửa đổi số của các trường được hỗ trợ; sử dụng mã Mod khi cần logic mới.
4. Địa chỉ trò chơi gốc, thứ tự byte, danh tính lớp phủ và cấu trúc bên trong tập trung ở lớp thích ứng trò chơi. Giao diện chung sử dụng ID ổn định, đối tượng giá trị, bộ xử lý phiên bản thế hệ và vòng đời rõ ràng.
5. Đầu tiên hỗ trợ phạm vi bao phủ các trường đã biết của đối tượng ban đầu, sau đó hỗ trợ các đối tượng và cấp độ mới; việc thêm ID mới yêu cầu xác minh mảng, chỉ mục và dung lượng lưu trữ ban đầu.

## 2. Cấu trúc code đáng tham khảo

### N64ModernRuntime: Tái sử dụng cơ sở hạ tầng Mod

Phần phụ thuộc cố định cục bộ và phần thượng nguồn của xác minh này đều là `cdf5abbd5026fef5c364c676e4667c45e42b6863`. `librecomp` đã chứa bản kê khai Mod, phần phụ thuộc, thay thế hàm/móc/sự kiện, nhập/xuất và đăng ký loại nội dung. `ModContentType` cung cấp lệnh gọi lại để bật, tắt, sắp xếp các thay đổi và chuyển đổi thời gian chạy; phù hợp để đăng ký nội dung ngôn ngữ, dữ liệu và tài nguyên riêng của SRW64 trong cùng cơ chế quản lý gói.

Tham khảo: [Loại nội dung và giao diện Mod](https://github.com/N64Recomp/N64ModernRuntime/blob/cdf5abbd5026fef5c364c676e4667c45e42b6863/librecomp/include/librecomp/mods.hpp) · [Hướng dẫn viết Mod](https://hackmd.io/fMDiGEJ9TBSjomuZZOgzNg) · [Mẫu Mod Pasture](https://github.com/HarvestMoon64Recomp/HM64RecompModTemplate).

Bạn nên tiếp tục sử dụng chuỗi công cụ `.nrm` Code Mod ngược dòng, được bổ sung bằng các mẫu ký hiệu và xuất phiên bản SRW64. Lược đồ ngôn ngữ/dữ liệu, quy tắc hợp nhất và ngữ nghĩa lưu trữ vẫn cần được bạn tự triển khai; Xung đột thay thế chức năng nhận dạng ngược dòng không có nghĩa là có thể xác định hai gói sửa đổi HP của cùng một cơ thể cùng một lúc.

### RecompFrontend: Mượn menu và mô-đun đầu vào

Xác minh cam kết `b1a1477c6556aeb7ed45defbfb5924f721efebc1`. `recompinput` của nó quản lý bàn phím, chuột, tay cầm và ánh xạ; `recompui` quản lý cài đặt, menu Mod và giao diện người dùng tự xây dựng của Mod, đồng thời sử dụng RmlUi và RT64/plume nội bộ. [Mô tả dự án](https://github.com/N64Recomp/RecompFrontend/blob/b1a1477c6556aeb7ed45defbfb5924f721efebc1/README.md)

Nó phù hợp làm ứng cử viên tích hợp cho trình khởi chạy, đầu vào và menu quản trị. Kiểu sắp chữ hội thoại hiện tại của SRW64 (một công cụ văn bản đa nền tảng) và tính năng tổng hợp Metal sẽ vẫn nằm trong phần phụ trợ của nền tảng, với văn bản được cung cấp thông qua dịch vụ đa ngôn ngữ thống nhất. Quá trình kiểm tra này không tìm thấy dịch vụ thư mục đa ngôn ngữ hoàn chỉnh được tạo sẵn và quyền truy cập vào RecompFrontend không thể được coi là chuyển đổi Nhật-Trung. Nguyên mẫu tích hợp cần xác minh mức tiêu thụ đầu vào, thứ tự hiển thị và cập nhật ngôn ngữ cho cả hai lớp giao diện người dùng.

### Wesnoth: Dựa trên sự tách biệt giữa nội dung và ngôn ngữ trong cờ chiến

Wesnoth không phải là một bản tổng hợp lại, nhưng nó xác định ID duy nhất của đơn vị, tên có thể dịch được, hình ảnh, khả năng và vũ khí tương ứng; các cấp độ được kết nối với cấp độ tiếp theo thông qua ID, bản đồ, trại, sự kiện và nội dung bổ sung có thể có các trường dịch độc lập. Điều này tương tự với mục tiêu của SRW64 là “dữ liệu cơ thể/nhân vật + cấp độ + mở rộng đa ngôn ngữ”.

Tham khảo: [Định nghĩa đơn vị](https://wiki.wesnoth.org/UnitTypeWML) · [Định nghĩa cấp độ](https://wiki.wesnoth.org/ScenarioWML) · [Bản dịch nội dung bổ sung](https://wiki.wesnoth.org/GettextForWesnothDevelopers).

Dựa trên ý tưởng miền dịch và phân lớp nội dung, phiên bản đầu tiên tiếp tục sử dụng chuỗi công cụ JSON hiện có của dự án này để tránh giới thiệu toàn bộ bộ công cụ WML cho các tệp cấu hình.

## 3. Phá dỡ ranh giới và công trình còn lại

2026-09-12 Đường dẫn ROM cũ của Trung Quốc đã bị xóa. Phân tích cú pháp ban đầu ở `src/srw64_rom/`,
Ánh xạ glyph tiếng Nhật có khóa nguồn độc lập, thư mục ngôn ngữ, TextKey và hồ sơ JP thống nhất được đặt trong
`src/srw64_native/`. Trang tên gốc sử dụng mã hóa tên trò chơi gốc và không còn dựa vào phân bổ glyph của bản vá ROM nữa.

Vẫn cần phải tiếp tục tách biệt việc sắp chữ văn bản và vẽ nền tảng, khôi phục các trình tiêu dùng văn bản trò chơi khác và tích hợp nội bộ
`SRW64GameHooks` được chuyển đổi thành một sự kiện ngữ nghĩa mà Mod có thể sử dụng. Khe cắm hiện tại và giao diện RDRAM
Nó tiếp tục thuộc về lớp thích ứng nội bộ; nó không thể được sử dụng trực tiếp như một SDK công khai. Xem [Hướng dẫn phát triển bản địa](../guide/native-development.md) để biết trách nhiệm thực tế.

## 4. Ranh giới mô-đun được đề xuất

Danh mục đề xuất, chỉ để thể hiện trách nhiệm:

```text
src/native/
  app/                 启动、PlayProfile、设置、模块生命周期
  game_adapter/        日版资源/地址映射、overlay、数据读写与原脚本桥接
  content/             包解析、schema、内容注册表、合并和来源记录
  localization/        TextKey、目录、回退、格式参数、语言配置
  presentation/        对话与界面模型、资源解析、模型替换接口
  platform/macos/      Metal 合成与菜单栏
  mod_api/             版本化导出、语义事件与命令
tools/content/         提取、校验、导入导出、打包、差异报告
```

Máy chủ tiếp tục sử dụng các loại giá trị C++ và ảnh chụp nhanh bất biến trong nội bộ. Các giao diện cần vượt qua `.nrm` hoặc ranh giới thư viện động sử dụng loại có chiều rộng cố định, độ dài và phiên bản rõ ràng, đồng thời không xuất vùng chứa C++ STL hoặc cấu trúc bộ nhớ trò chơi gốc.

Luồng dữ liệu: ROM tạo nội dung cơ bản thông qua lớp thích ứng; trình quản lý gói hợp nhất phạm vi nội dung; lớp thích ứng trả về các trường hợp lệ cho trò chơi gốc tại thời điểm tải đã xác minh. Giao diện người dùng đọc từ cùng tải trọng với ảnh chụp nhanh đang chạy và dịch vụ ngôn ngữ cuối cùng sẽ phân tích cú pháp văn bản để hiển thị. Phải xác minh rằng các thay đổi về số được sử dụng bởi logic chiến đấu và không thể chỉ cập nhật bảng dữ liệu.

## 5. Thiết kế đa ngôn ngữ

### 5.1 Ngôn ngữ và cách trình bày độc lập với nhau

- Phiên bản đầu tiên của ngôn ngữ là `ja` và `zh-Hans`; `zh-Hant`, `en`, v.v. có thể được thêm vào trong tương lai. Thẻ ngôn ngữ được coi là dữ liệu và các nhánh C++ không được xây dựng cho từng ngôn ngữ.
- Văn bản trò chơi gốc của `ja` được xuất từ ROM gốc cục bộ của người dùng sang một thư mục; các chuỗi tiếng Nhật và tiếng Trung mới được thêm vào của giao diện người dùng gốc sẽ được dự án duy trì. Các hình tượng không xác định sẽ giữ lại nhận dạng hình tượng ban đầu và khả năng dự phòng.
- Kiểu chữ gốc và bố cục gốc là các tùy chọn trình bày riêng biệt. Bản đồ HD, mô hình hiện đại và phông chữ gốc cũng có sẵn khi chọn tiếng Nhật.
- Văn bản được nướng trong ảnh thuộc về tài nguyên ngôn ngữ. Không thể chia sẻ hình đại diện/bản đồ văn bản; Không thể bật nhãn dán tiếng Trung và tập bản đồ phông chữ tiếng Trung vô điều kiện ở chế độ tiếng Nhật.
- Phông chữ, dự phòng, ngắt dòng và hướng viết được xử lý bằng cấu hình ngôn ngữ và phần phụ trợ văn bản. Ấn bản đầu tiên được xác nhận là ở Nhật Bản; các ngôn ngữ trong tương lai không có nghĩa là tất cả các hệ thống chữ viết phức tạp đều được chấp nhận.

### 5.2 Phím văn bản và luồng điều khiển ổn định

Khóa văn bản gốc giữ lại ID bảng và bản ghi, chẳng hạn như `base:t00_17412`; Mod mới sử dụng không gian tên riêng của nó, chẳng hạn như `example.campaign:dialogue.intro.001`. Tên, menu và lời nhắc hệ thống cũng sử dụng cùng khái niệm TextKey và được duy trì trong các thư mục riêng biệt.

Các đoạn văn bản gốc được chuyển đổi thành các thông báo có cấu trúc: các đoạn văn bản, các tham số được đặt tên, các ký tự chuyên dụng và các rào cản tập lệnh được tách riêng. STOP/END và tiến bộ của trình thông dịch gốc thuộc về siêu dữ liệu của chương trình; tác giả dịch chỉ sửa đổi những đoạn tương ứng và vị trí tham số được phép. Có thể thêm tính năng phân trang/đọc từ tự động nhưng không thể vượt quá rào cản tập lệnh gốc. Thêm hoặc xóa các sự kiện trong câu chuyện là một mod cấp độ.

Việc xuất bản dịch phải bao gồm văn bản gốc, TextKey, số đoạn, người nói/cảnh (khi được nhận dạng), mô tả tham số, tóm tắt phiên bản nguồn, bản dịch và trạng thái đánh giá; ảnh chụp màn hình có thể được thêm vào để liên kết. Phiên bản đầu tiên sử dụng JSON và cung cấp tính năng nhập và xuất PO làm công cụ đóng góp tiếp theo. Tất cả các định dạng được biên dịch vào cùng một thư mục thời gian chạy.

### 5.3 Gói ngôn ngữ cộng đồng và dự phòng

Khi trò chơi cơ bản bị thiếu bản dịch, nó sẽ quay trở lại bản ghi nguồn tiếng Nhật tương ứng; khi Mod mới thiếu dịch sẽ quay về ngôn ngữ nguồn do tác giả nội dung khai báo. Các bên thứ ba có thể xuất bản các gói dịch riêng biệt, nêu rõ gói nội dung nào được dịch và phiên bản nào có thể áp dụng mà không cần sao chép dữ liệu nội dung hoặc cấp độ của chúng.

Thứ tự phân tích cú pháp là "xác định gói chứa nội dung và bản ghi nguồn cuối cùng → chọn ghi đè hiệu quả của ngôn ngữ tương ứng với bản ghi → ngôn ngữ nguồn của gói". Ngôn ngữ nguồn cuối cùng của văn bản cơ bản là tiếng Nhật; chiến dịch tùy chỉnh có thể được chọn. Khi văn bản nguồn hoặc cấu trúc điều khiển thay đổi, dấu dịch cũ cần được cập nhật; các đoạn không hợp lệ sẽ quay trở lại văn bản nguồn và được báo cáo, đồng thời không thể thay đổi tập lệnh một cách âm thầm.

Phiên bản đầu tiên chọn ngôn ngữ trong giai đoạn khởi động/tiêu đề và tạo một thư mục không thể thay đổi khi khởi động. Tính năng chuyển đổi nóng trong trò chơi được duy trì cho đến khi các chiến lược chờ đối thoại, phân trang và vô hiệu hóa cảnh được xác minh; bạn không thể chỉ xóa kết cấu và giữ phân trang ngôn ngữ cũ.

Tên hiển thị ký tự mặc định theo ngôn ngữ; tên do người dùng thay đổi vẫn giữ nguyên đầu vào ban đầu. Trong kho lưu trữ gốc, rất khó để xác định liệu tên có phải là mặc định hay không và giá trị ban đầu có được giữ lại hay không. Nó không thể được suy ra bởi "chính xác bằng chuỗi mặc định". Việc nhập và duy trì tên Unicode tùy ý được thiết kế độc lập và phiên bản chuyển đổi ngôn ngữ đầu tiên không yêu cầu thay đổi định dạng lưu trữ tên gốc.

2026-09-11 [Nguyên mẫu nhập tên gốc](../native/native-name-entry.md) đã được thêm: hộp nhập hệ thống đảm nhận việc chỉnh sửa tên mở đầu, hỗ trợ nhập trực tiếp trong ký tự ROM gốc và giữ lại trường tên gốc và xác minh. Việc lưu trữ các tên và phần mở rộng Unicode tùy ý vẫn đang được tiến hành.

## 6. Content Mod: Từ các trường đã biết đến các cấp độ hoàn thành

### 6.1 Sổ đăng ký nội dung thống nhất

Tạo các loại rõ ràng: `UnitDef`, `PilotDef`, `WeaponDef`, `StageDef`, `AssetRef` và `TextKey`. Định nghĩa được tách biệt khỏi phiên bản đang chạy: HP cơ bản của máy thuộc về UnitDef; HP hiện tại, sức mạnh và trạng thái hành động của cấp độ này thuộc về thể hiện.

Đối tượng ban đầu giữ lại ID cơ sở ổn định và đối tượng mới sử dụng không gian tên tác giả. Lớp dưới cùng có thể được chuyển đổi thành chỉ mục số nguyên nhỏ gọn, nhưng ánh xạ cần có khả năng lưu và xác minh và không thể thay đổi theo thứ tự quét gói. Các trường có ngữ nghĩa chưa được nhận dạng sẽ giữ lại dữ liệu và nguồn gốc không rõ ràng, cấm đoán tên hoặc cho phép sắp xếp lại tùy ý.

Việc sửa đổi các đối tượng hiện có sẽ ưu tiên ghi đè trường hơn, với các xác nhận tóm tắt bản ghi nguồn/giá trị cũ tùy chọn. chỉ ra:

```json
{
  "target": "base:unit/<verified-id>",
  "expect": { "hp": 8000 },
  "set": { "hp": 9000 }
}
```

Ví dụ trên chỉ thể hiện giao diện được đề xuất và cần phải xác minh ID và ánh xạ trường. Sự thích ứng cơ bản chịu trách nhiệm về phạm vi, bố cục, giá trị dẫn xuất và thời gian ứng dụng; khi sửa đổi HP tối đa, cũng cần phải chỉ định việc xử lý HP hiện tại của đơn vị được tạo/kho lưu trữ cũ, không thể được coi ngầm là xử lý.

Có thể hợp nhất các sửa đổi đối với các trường khác nhau trong hai gói; những sửa đổi đối với cùng một trường yêu cầu các mối quan hệ đưa tin rõ ràng hoặc xung đột báo cáo. Mỗi giá trị cuối cùng ghi lại gói nguồn và chuỗi thay đổi. Đừng đặt thứ tự thư mục hoặc bất kỳ quy tắc mặc định nào tùy tiện "người cuối cùng được tải sẽ thắng".

### 6.2 Cấu trúc gói

Gói nội dung đề xuất:

```text
example.campaign/
  manifest.json
  data/units.json
  data/pilots.json
  data/weapons.json
  stages/intro.json
  locales/ja.json
  locales/zh-Hans.json
  assets/
```

Bản kê khai tái sử dụng ID gói, phiên bản, trò chơi mục tiêu và các trường phụ thuộc được hỗ trợ bởi thượng nguồn; siêu dữ liệu bổ sung của dự án thể hiện lược đồ, ngôn ngữ nguồn, khả năng nội dung và khả năng tương thích cơ bản. Gói chỉ có thể có `locales/` hoặc chỉ nội dung. Không gian tên gói được sở hữu hợp lý và không phụ thuộc vào tên tệp đĩa của nó.

Phiên bản đầu tiên chỉ cần đăng ký loại nội dung dữ liệu, chế độ phát triển thư mục và lối vào đóng gói. Các mod mã tiếp tục đi lên `.nrm`, tránh nhu cầu duy trì bộ tải bản vá chức năng thứ hai. Đối với những tác giả chỉ thay đổi giá trị ngôn ngữ/số thì không cần phải cài đặt trình biên dịch C++.

### 6.3 Các cấp độ được mở theo từng lớp

1. **Phạm vi bao phủ thông số cấp độ ban đầu**: Đơn vị tấn công, trại, vị trí ban đầu, trường tiếp viện và phần thưởng đã được xác minh.
2. **Chỉnh sửa sự kiện có cấu trúc**: Bản đồ, hoạt động triển khai, điều kiện, hành động, tham chiếu đối thoại và mối quan hệ thắng thua được tách riêng và chuyển đổi thành các thao tác tập lệnh gốc dễ hiểu hoặc lệnh gọi cầu nối gốc đã được xác minh.
3. **Cấp độ/chiến dịch mới**: Nó sẽ được mở sau khi hoàn thành việc phân bổ ID giai đoạn, chuyển cấp, kế thừa nhóm, trạng thái sự kiện, tiết kiệm và vòng đời tài nguyên.

Giữ trình thông dịch tập lệnh gốc chạy ngữ nghĩa. Đầu tiên, máy chiết hoàn thành một chuyến đi khứ hồi không sửa đổi; các khu vực chứa các opcode không xác định, các bước nhảy chưa được giải quyết hoặc các phần phụ thuộc tái định vị được giữ lại dưới dạng các khối mờ đục, hạn chế các hoạt động có thể chỉnh sửa của chúng. Phiên bản đầu tiên không giới thiệu trình thông dịch Lua phổ quát để thay thế hệ thống cốt truyện gốc. Bắt đầu từ ngày 12 tháng 9 năm 2026, các hướng dẫn, khối điều kiện, dấu ngữ cảnh và loại trình kích hoạt của tập lệnh gốc có thể được đọc tĩnh (xem [Phân tích hoàn chỉnh các tập lệnh cấp độ](../script/stage-script-exploration.md)); việc so sánh viết lại và chạy vẫn chưa bắt đầu.

Máy bay mới cũng được triển khai theo từng giai đoạn: những thay đổi đối với dữ liệu hiện có có sẵn sớm nhất; các mục mới phải kiểm tra giới hạn mảng, tham chiếu vũ khí/nhân vật, AI, xoay danh sách và chỉ mục lưu trữ. recomp cho phép sửa đổi các giới hạn này, nhưng bản thân sổ đăng ký JSON không tự động mở rộng chúng.

## 7. Mod API và vòng đời trò chơi

Lớp thích ứng bên trong đọc và ghi trạng thái trò chơi một cách thống nhất, hiển thị các ảnh chụp nhanh chỉ đọc và các lệnh rõ ràng. Các sự kiện được đề xuất bao gồm `stage_entered`, `unit_selected`, `dialogue_segment_ready`, `battle_resolved`; xác định giai đoạn kích hoạt, trình tự, thời gian tồn tại của tham số và liệu có cho phép gửi lệnh hay không.

Phạm vi dữ liệu và các sự kiện quan sát chỉ đọc trong phiên bản đầu tiên của giai đoạn tải mở. Lệnh gọi lại giao diện người dùng chỉ có thể gửi yêu cầu và chuỗi trò chơi được sử dụng vào những thời điểm xác định; luồng kết xuất không trực tiếp sửa đổi RDRAM. Việc thay thế các quy tắc cốt lõi như thiệt hại sau đó sẽ được mở thông qua một giao diện được phiên bản riêng biệt và sẽ không được giải quyết nhiều lần thông qua nhiều lệnh gọi lại sự kiện theo bất kỳ trình tự nào.

Trình xử lý phiên bản công khai có một thế hệ và sẽ không hợp lệ sau khi chuyển đổi, đọc tệp và thoát. Có một trình tự rõ ràng cho các hoạt động lưu trữ, tải nội dung và khởi tạo cảnh; nhiều người đăng ký cho cùng một sự kiện được quản lý bởi lớp thích ứng và các Mod mới không thể ghi đè các móc đối thoại gốc hiện có.

Phiên bản API Mod, phiên bản lược đồ dữ liệu và phiên bản cơ sở của trò chơi được ghi riêng. Các bản vá chức năng trực tiếp cấp thấp vẫn có sẵn dưới dạng phần mở rộng cấp cao, nhưng khả năng tương thích địa chỉ/ký hiệu của chúng yêu cầu ràng buộc rõ ràng với phiên bản; tác giả nội dung thông thường sử dụng ID và trường ổn định.

## 8. Lưu trữ và cấu hình gói

Tài nguyên ngôn ngữ và chỉ hiển thị thuộc về cấu hình hiển thị và mục tiêu là chuyển đổi ngôn ngữ mà không thay đổi trạng thái cấp độ, số ngẫu nhiên hoặc nội dung lưu ban đầu. Dữ liệu trò chơi và gói cấp độ tạo thành cấu hình nội dung, ID bản ghi, phiên bản, tóm tắt nội dung hiệu quả và ánh xạ ID phiên bản.

Bản lưu tương thích ban đầu tiếp tục giữ lại dữ liệu SRAM gốc; trạng thái mở rộng có thể được đặt trong một sidecar/thùng chứa đã được phiên bản, được liên kết với thế hệ lưu và hàm băm ban đầu, đồng thời được hình thành nguyên tử thành một bộ lưu. Nếu mã hoặc nội dung Mod bị thay đổi, nó sẽ vẫn tồn tại. Bạn không thể khẳng định rằng nó chỉ ảnh hưởng đến màn hình.

Kiểm tra gói trò chơi và bản đồ khi tải. Khi thiếu gói đơn vị hoặc cấp độ mới, một báo cáo thiếu rõ ràng và mục khôi phục cấu hình sẽ được cung cấp. ID không xác định không thể được coi là một đơn vị khác để tiếp tục thực thi. Các kho lưu trữ thử nghiệm cũ của Trung Quốc giai đoạn 1 bao gồm các hình tượng và đường dẫn tên độc quyền, đồng thời việc di chuyển sang đường cơ sở JP thống nhất yêu cầu xác nhận đặc biệt; không được tự động coi là có thể hoán đổi cho nhau.

## 9. Trình tự thực hiện và nghiệm thu

1. **Cơ bản về ngôn ngữ**: Trích xuất TextKey, thư mục nguồn tiếng Nhật độc lập và thư mục zh-Hans; loại bỏ mã hóa cứng phông chữ/ngôn ngữ; chạy qua cảnh tương tự trên ROM gốc tiếng Nhật với lựa chọn giữa ngày, thiếu bản dịch dự phòng và bố cục phông chữ gốc. Sử dụng các mẫu tiếng Trung hiện có làm đầu vào di chuyển và giữ lại bằng chứng chấp nhận ban đầu.
2. **Gói và Cấu hình**: Kết nối với cơ chế loại nội dung Mod hiện có để tạo gói ngôn ngữ, gói tài nguyên thuần túy và PlayProfile hợp nhất. Việc thêm mẫu ngôn ngữ thứ ba chỉ thay đổi dữ liệu và không biên dịch lại máy chủ.
3. **Lược đồ và công cụ khung máy bay/Nhân vật/Vũ khí**: Trước tiên hãy trích xuất, xác minh và báo cáo sự khác biệt, sau đó tải và ghi đè một trường đã biết để chứng minh rằng menu gốc, chiến đấu thực tế cũng như các tệp được lưu và đọc là nhất quán. Trình chỉnh sửa sử dụng cùng một lược đồ và trình xác thực.
4. **SDK cấp độ và công khai**: Trước tiên, hãy xác minh quá trình triển khai/sự kiện ở cấp độ ban đầu, sau đó tạo mẫu phạm vi cấp độ tối thiểu; khi giao diện thực sự được sử dụng bởi hai mẫu độc lập, hãy phát hành SDK, mẫu và câu lệnh tương thích.

Kiểm tra chính: Các sự kiện kiểm soát là nhất quán giữa Nhật Bản và Trung Quốc trong cùng một hoạt động; chuyển đổi ngôn ngữ không thay đổi dữ liệu trò chơi; ID văn bản có cùng tên không xung đột khi chúng nằm trong các bảng khác nhau; tham số mẫu và xác minh STOP/END; hết hạn dịch và dự phòng từ bị thiếu; sự chắc chắn trong việc phân loại gói và xung đột trường; Giá trị UI phù hợp với việc giải quyết; thiếu xử lý kho lưu trữ Mod/cũ. Việc chấp nhận nội dung mới phải bao gồm trò chơi thực tế và việc chuyển lược đồ tĩnh chỉ chứng minh rằng định dạng này là hợp pháp.

2026-09-11 Nền tảng chuyển đổi cấu hình/tài nguyên phát triển ở bước 1 và 2 đã được triển khai; đăng ký loại nội dung, phạm vi bao phủ trường trò chơi, cấp độ và SDK công khai vẫn chưa được triển khai. Phạm vi chính xác hiện có và mức độ chấp nhận nằm trong [Triển khai lần đầu](../native/native-content-foundation.md).