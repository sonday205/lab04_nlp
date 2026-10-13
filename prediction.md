# Prediction trước experiment


### Prediction 1: TF-IDF + Logistic Regression có hoạt động tốt không?
- **Prediction:** Có.
- **Reason:** TF-IDF biểu diễn tốt các từ đặc trưng, Logistic Regression phù hợp với dữ liệu sparse.
- **Confidence:** High (90%).

### Prediction 2: Average Word2Vec có chắc chắn tốt hơn TF-IDF không?
- **Prediction:** Không.
- **Reason:** Average Word2Vec có thể làm mất thông tin từ quan trọng và thứ tự từ.
- **Confidence:** High (90%).

### Prediction 3: Tăng vocabulary size thì accuracy chắc chắn tăng không?
- **Prediction:** Không.
- **Reason:** Vocabulary lớn có thể thêm nhiễu, tăng độ phức tạp và gây overfitting.
- **Confidence:** High (95%).

### Prediction 4: Bỏ stopwords thì performance chắc chắn tăng không?
- **Prediction:** Không.
- **Reason:** Một số stopwords như "not" mang ý nghĩa quan trọng trong sentiment classification.
- **Confidence:** High (95%).

### Prediction 5: Accuracy và F1 có thể cho kết luận khác nhau không?
- **Prediction:** Có.
- **Reason:** Với dữ liệu mất cân bằng, accuracy có thể cao dù mô hình dự đoán kém ở class thiểu số.
- **Confidence:** High (95%).
