# LAB 04 — Text Classification với IMDb


## Chạy

Chọn `.venv/bin/python` trong VS Code, mở `classification.ipynb` và **Run All**.
Notebook đọc kết quả đã chạy và thực hiện lại pipeline baseline; đặt `RUN_EXPERIMENTS = True` để huấn luyện lại toàn bộ.

Chạy từ đầu trong thư mục `lab04_nlp`:

```bash
.venv/bin/python preprocessing.py
PYTHONHASHSEED=42 .venv/bin/python experiments.py
```

Demo sentiment với mô hình đã lưu:

```bash
.venv/bin/python predict.py "The acting was excellent." "This movie was boring."
```

Nếu chuyển sang máy khác:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

## Đối chiếu yêu cầu PDF

| Mục trong PDF | File/kết quả |
|---|---|
| 6–9: Bài tính toán | `calculations.pdf`: bài làm viết tay; `calculations.md`: khung đối chiếu |
| 5, 10: Prediction | `prediction.md`: Prediction/Reason/Confidence do bạn cung cấp |
| 11: Dataset inspection | Notebook, `data/inspection.json`, biểu đồ nhãn/độ dài |
| 12: Split, leakage | Stratified 60/20/20; nhận xét trong `reflection.md` |
| 13–14: Core, baseline | Code fit/transform/LR trong notebook; số đo trong `results.csv` |
| 15–16: Representation | TF-IDF + LR, Average Word2Vec + LR, TF-IDF + Linear SVM |
| 17: Phủ định | Dự đoán good/not good, bad/not bad và cosine similarity |
| 18: n-gram | Unigram so với unigram + bigram; vocabulary, F1, thời gian |
| 19–20: Evaluation | Accuracy, precision, recall, F1, macro-F1 và confusion matrix |
| 21: Error analysis | 3 review đúng, 3 review sai; nhận xét rút gọn trong `error_analysis.md` |
| 22: Model weights | Top positive/negative features trong notebook và `artifacts/top_features.csv` |
| 23: Application | Sentiment classification: notebook và `predict.py` |
| 24: AI statement | Cuối README |
| 25: Learning check | Câu hỏi và chỗ trống trong `reflection.md` |
| 26: Deliverables | Đủ tên file yêu cầu; bài viết tay và prediction của sinh viên được giữ |

Thêm khảo sát vocabulary cap 5k/20k/50k và bỏ/giữ stopwords để sinh viên đối chiếu prediction.

## Cấu hình và cách đánh giá

- Chuẩn hóa HTML, khoảng trắng, chữ thường bằng quy tắc cố định; giữ review gốc và ID dòng. Loại nội dung trùng trước split. Nếu có nội dung mang nhãn mâu thuẫn, loại cả nhóm.
- Seed 42; stratify theo nhãn; kiểm tra không trùng nội dung hoặc ID giữa các tập. Số mẫu sau làm sạch: train 29.746, validation 9.916, test 9.916.
- TF-IDF: `min_df=2`; unigram hoặc unigram + bigram. Các cấu hình mặc định giữ stopwords; thí nghiệm riêng dùng danh sách `english` của sklearn.
- Word2Vec chỉ học từ train: Skip-gram, 100 chiều, window 5, min_count 2, negative 5, epochs 5, workers 1. Document vector là trung bình các từ trong vocabulary; bỏ qua OOV, không có từ hợp lệ thì dùng vector 0. Coverage được lưu.
- LR: liblinear, max_iter 2000. SVM: LinearSVC, max_iter 5000. Chọn C ∈ {0.5, 1, 2} bằng F1 validation; có bảng validation với C=1 cố định để so sánh representation.
- Khóa mô hình application theo validation trước khi đánh giá test; không refit train + validation. Không dùng test để chọn lại cấu hình.
- Precision/recall/F1 binary lấy positive làm lớp dương; macro-F1 trung bình đều hai lớp. LR dùng threshold mặc định 0.5. Probe phủ định chỉ gồm bốn câu minh họa.
- Thời gian train = fit representation + fit classifier của cấu hình được chọn; không gồm đọc file, tokenization, transform/lấy trung bình embeddings, toàn bộ tuning hoặc ghi file. BLAS giới hạn hai thread.

## File kết quả

- `classification.ipynb`: các thí nghiệm có output và code baseline trực tiếp.
- `preprocessing.py`, `experiments.py`, `predict.py`: xử lý dữ liệu, huấn luyện/đánh giá, demo.
- `results.csv`, `confusion_matrix.png`: số đo test và ma trận mô hình được chọn bằng validation.
- `data/`: train/validation/test CSV, thống kê và biểu đồ dataset.
- `artifacts/`: validation results, selected configs, predictions, classification reports, confusion matrices, weights, phủ định, coverage và mô hình đã lưu.
- `artifacts/run_manifest.json`: cấu hình, phiên bản thư viện và SHA-256 cho lần chạy.

## Phần sinh viên tự điền

Bài viết tay nằm trong `calculations.pdf`; 5 prediction bạn cung cấp nằm trong `prediction.md`, `reflection.md` và `error_analysis.md`; các nguyên nhân lỗi vẫn là giả thuyết cần kiểm tra bằng review đầy đủ.

## AI assistance statement

- Tool: Codex.
- Purpose: hỗ trợ preprocessing, sử dụng sklearn/gensim, visualization, debugging và rút gọn nội dung có sẵn trong ZIP.
- Generated: code thí nghiệm, notebook, biểu đồ và khung bài tự làm.
- Modified: rút gọn code chọn C bị lặp, bổ sung baseline và các file còn thiếu; nhập và rút gọn phần nhận xét từ `lab04_completed.zip`. Bản nhận xét trong ZIP ghi nhận đã được ChatGPT hỗ trợ tạo.
- Verified: trước đó đã chạy thí nghiệm/notebook và kiểm tra metrics/inference. 
