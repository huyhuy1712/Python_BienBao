import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from keras.models import Model
from keras.layers import Dense, Flatten, Dropout, BatchNormalization, GlobalAveragePooling2D
from keras.applications import MobileNetV2
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import EarlyStopping
import os

# 🔹 **Chuẩn bị dữ liệu**
data = []
labels = []
classes = 43  # Số lượng class
cur_path = os.getcwd()

for i in range(classes):
    path = os.path.join(cur_path, 'IMGtrain', str(i))
    images = os.listdir(path)

    for a in images:
        try:
            image = Image.open(os.path.join(path, a)).convert('RGB')
            image = image.resize((100, 100))
            image = np.array(image)

            if image.shape == (100, 100, 3):
                data.append(image)
                labels.append(i)
            else:
                print(f"Ignoring image {a} with invalid shape: {image.shape}")
        except Exception as e:
            print(f"Error loading image {a}: {e}")

# 🔹 **Chuyển danh sách thành mảng numpy và chuẩn hóa dữ liệu**
data = np.array(data) / 255.0  # Đưa pixel về khoảng [0,1]
labels = np.array(labels)

# 🔹 **Chia tập dữ liệu train/test**
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=43)

# 🔹 **One-hot encoding cho nhãn**
y_train = to_categorical(y_train, classes)
y_test = to_categorical(y_test, classes)

# 🔹 **Data Augmentation để tránh overfitting**
datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)
datagen.fit(X_train)

# 🔹 **Sử dụng Transfer Learning (MobileNetV2)**
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(100, 100, 3))

# 🔹 **Thêm các lớp Fully Connected**
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(512, activation='relu')(x)
x = Dropout(0.5)(x)
x = Dense(256, activation='relu')(x)
x = Dropout(0.5)(x)
x = Dense(classes, activation='softmax')(x)

# 🔹 **Tạo mô hình mới**
model = Model(inputs=base_model.input, outputs=x)

# 🔹 **Đóng băng các lớp của MobileNetV2 để giữ trọng số đã học**
for layer in base_model.layers:
    layer.trainable = False

# 🔹 **Compile mô hình**
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# 🔹 **Early Stopping để tránh overfitting**
early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

# 🔹 **Huấn luyện mô hình**
epochs = 50  # Có thể tăng lên nếu cần
history = model.fit(datagen.flow(X_train, y_train, batch_size=64),
                    epochs=epochs,
                    validation_data=(X_test, y_test),
                    callbacks=[early_stopping])

# 🔹 **Lưu model vào thư mục**
save_dir = os.path.join(cur_path, 'models_train')
os.makedirs(save_dir, exist_ok=True)

existing_models = [f for f in os.listdir(save_dir) if f.startswith("my_model") and f.endswith(".keras")]
model_number = len(existing_models) + 1
model_filename = f"my_model{model_number}.keras"
model_path = os.path.join(save_dir, model_filename)
model.save(model_path)
print(f"Model saved at: {model_path}")

# 🔹 **Lưu biểu đồ Accuracy**
graph_dir = os.path.join(cur_path, 'train_graphs')
os.makedirs(graph_dir, exist_ok=True)

plt.figure(figsize=(8, 4))
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.savefig(os.path.join(graph_dir, 'accuracy.png'))
plt.close()

# 🔹 **Lưu biểu đồ Loss**
plt.figure(figsize=(8, 4))
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.savefig(os.path.join(graph_dir, 'loss.png'))
plt.close()

print(f"Graphs saved in: {graph_dir}")
