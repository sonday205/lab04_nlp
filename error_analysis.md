# Error analysis

Mô hình: `tfidf_bi_50k_LR`. Nội dung rút gọn từ `lab04_completed.zip`.
Review đầy đủ: `artifacts/error_examples.csv`. Các nguyên nhân dưới đây là giả thuyết cần kiểm tra.

| source_id | Nhãn thật | Dự đoán | Nhận xét ngắn |
|---|---|---|---|
| 14141 | negative | negative | Có cụm thể hiện chất lượng phim giảm. |
| 4254 | negative | negative | Có các từ chê phim rõ ràng. |
| 9212 | negative | negative | Mô tả trải nghiệm xem phim tiêu cực. |
| 44794 | negative | positive | Có thể nhầm do khen diễn viên nhưng chê phim. |
| 33874 | negative | positive | Đoạn đầu chủ yếu kể nội dung; chưa đủ để xác định nguyên nhân. |
| 21480 | negative | positive | Có thể liên quan đến phủ định và so sánh. |

Các ví dụ này đều có nhãn thật negative, nên chưa đại diện cho cả hai lớp.

Nhận xét sau khi đọc toàn bộ review: __________
