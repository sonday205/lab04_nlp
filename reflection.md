# Nhận xét và reflection


## Dữ liệu và leakage

Dữ liệu tương đối cân bằng. Đã xử lý review trùng và chia 60/20/20. Chỉ học vocabulary, IDF và Word2Vec trên train.

## So sánh representation

TF-IDF giữ các từ đặc trưng nên phù hợp với bài toán này. Average Word2Vec có thể làm loãng thông tin khi lấy trung bình. Kết quả không đại diện cho mọi dataset.

## Phủ định và n-gram

Bigram giúp giữ một số cụm như `not good`, nhưng chưa xử lý được mọi dạng phủ định. Đổi lại, số đặc trưng và thời gian xử lý tăng.

## Vocabulary và stopwords

Tăng vocabulary không đảm bảo kết quả luôn tốt hơn. Bỏ stopwords có thể làm mất thông tin cần thiết.

## Đánh giá và trọng số

Cần xem cả accuracy, precision, recall, F1 và confusion matrix. Các feature nổi bật phần lớn phù hợp với sentiment, nhưng trọng số còn phụ thuộc dữ liệu.

## Reflection

Representation ảnh hưởng đến kết quả phân loại. Mô hình còn hạn chế với phủ định và ngữ cảnh. Có thể thử mô hình xét thứ tự từ ở các bài tiếp theo.
