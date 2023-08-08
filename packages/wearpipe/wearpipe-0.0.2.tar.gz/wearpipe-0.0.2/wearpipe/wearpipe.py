import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.preprocessing import LabelEncoder

def train_model(features, labels, n_classes, n_epochs=10, avg_method='macro'):
    """
    Parameters:
    features: Numpy array, the input data.
    labels: Numpy array, the target data.
    n_classes: int, the number of unique classes.
    n_epochs: int, the number of epochs to train for.
    avg_method: str, the averaging method to use for precision, recall, and F1-score.

    Returns:
    model: Keras model, the trained LSTM model.
    metrics: Dictionary, containing various ML metrics.
    """

    # Reshape input to be 3D [samples, timesteps, features]
    features = features.reshape((features.shape[0], 1, features.shape[1]))
    
    # Convert labels to categorical
    labels = to_categorical(labels, num_classes=n_classes)

    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
    
    # Initialize the model
    model = Sequential()
    model.add(LSTM(50, input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(Dense(n_classes, activation='softmax'))
    
    # Compile the model
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    
    # Train the model
    model.fit(X_train, y_train, epochs=n_epochs, verbose=2, shuffle=False)

    # Make predictions
    y_pred = model.predict(X_test)
    y_pred_classes = np.argmax(y_pred, axis=1)
    y_test_classes = np.argmax(y_test, axis=1)

    # Compute metrics
    accuracy = accuracy_score(y_test_classes, y_pred_classes)
    precision = precision_score(y_test_classes, y_pred_classes, average=avg_method)
    recall = recall_score(y_test_classes, y_pred_classes, average=avg_method)
    f1 = f1_score(y_test_classes, y_pred_classes, average=avg_method)

    metrics = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1
    }

    return model, metrics

def apply_model(df, feature_columns, model, le):
    """
    Parameters:
    df: DataFrame, the original data.
    feature_columns: list, the names of the feature columns.
    model: Keras model, the trained LSTM model.
    le: LabelEncoder, the label encoder used during training.

    Returns:
    df: DataFrame, the original DataFrame with additional columns for the model's predictions and their confidence.
    """

    # Extract features
    features = df[feature_columns].values

    # Reshape input to be 3D [samples, timesteps, features]
    features = features.reshape((features.shape[0], 1, features.shape[1]))
    
    # Make predictions
    predictions = model.predict(features)
    predictions_classes = np.argmax(predictions, axis=1)
    
    # Compute prediction confidences
    prediction_confidences = np.max(predictions, axis=1)
    
    # Transform class indices back into original labels
    predictions_labels = le.inverse_transform(predictions_classes)
    
    # Add predictions and their confidence to original DataFrame
    df['Predictions'] = predictions_labels
    df['Prediction_Confidence'] = prediction_confidences

    return df




def choi_non_wear(df, accx, accy, accz, sampling_rate, non_wear_time_threshold=60, std_threshold=0.013, range_threshold=0.05):
    """
    Parameters:
    df: DataFrame, the original data.
    sampling_rate: int, the number of data points per minute.
    non_wear_time_threshold: int, the time threshold (in minutes) to detect non-wear.
    std_threshold: int, the standard deviation threshold to detect non-wear.
    range_threshold: int, the range threshold to detect non-wear.

    Returns:
    df: DataFrame, the original data with an additional column 'Wear' which indicates periods of wear and non-wear.
    """
    acc_data = np.array([df[accx].values, df[accy].values, df[accz].values])
    wear_time = []

    for i in range(0, len(acc_data[0]), non_wear_time_threshold * sampling_rate):
        segment = acc_data[:, i:i+non_wear_time_threshold * sampling_rate]

        if len(segment[0]) < non_wear_time_threshold * sampling_rate:
            wear_time.extend([False] * len(segment[0]))
            continue

        std = np.std(segment, axis=1)
        acc_range = np.ptp(segment, axis=1)

        if np.all(std < std_threshold) and np.all(acc_range < range_threshold):
            wear_time.extend([False] * non_wear_time_threshold * sampling_rate)
        else:
            wear_time.extend([True] * non_wear_time_threshold * sampling_rate)

    df['Wear'] = np.where(wear_time, 'Wear', 'Non-Wear')

    return df

# Data preprocessing function
def preprocess_data(train_data, class_column, feature_columns):
    # Prepare features and labels
    features = train_data[feature_columns].values
    labels = train_data[class_column].values
    
    # Encode string labels into integers
    le = LabelEncoder()
    labels_encoded = le.fit_transform(labels)
    
    # Determine the number of unique classes
    n_classes = len(le.classes_)

    return features, labels_encoded, n_classes, le

def assess_performance(df, true_labels_col, predicted_labels_col):
    """
    Parameters:
    df: DataFrame, the original data.
    true_labels_col: str, the name of the column with the true labels.
    predicted_labels_col: str, the name of the column with the predicted labels.

    Returns:
    metrics: Dict, contains various performance metrics.
    conf_mat: Numpy array, the confusion matrix.
    """

    # Extract true and predicted labels
    true_labels = df[true_labels_col].values
    predicted_labels = df[predicted_labels_col].values

    # Compute metrics
    class_report = classification_report(true_labels, predicted_labels, output_dict=True)
    accuracy = class_report['accuracy']
    precision = class_report['macro avg']['precision']
    recall = class_report['macro avg']['recall']
    f1 = class_report['macro avg']['f1-score']
    metrics = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1
    }

    # Compute confusion matrix
    conf_mat = confusion_matrix(true_labels, predicted_labels)

    return metrics, conf_mat