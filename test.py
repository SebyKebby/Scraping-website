import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_percentage_error
import shap

# Load and prepare the data
def prepare_data(df):
    # Create interaction terms with TTDI
    df['ESG_env_TTDI'] = df['ESG environmental'] * df['TTDI Score']
    df['ESG_social_TTDI'] = df['ESG social'] * df['TTDI Score']
    df['ESG_gov_TTDI'] = df['ESG governmental'] * df['TTDI Score']
    
    # Select features
    features = ['ESG environmental', 'ESG social', 'ESG governmental',
                'TTDI Score', 'ESG_env_TTDI', 'ESG_social_TTDI', 'ESG_gov_TTDI',
                'D/E Ratio', 'Market Value']
    
    # Define performance metrics as targets
    performance_metrics = ['ROI (%)', 'ROE', 'ROA']
    
    return df[features], df[performance_metrics]

# Calculate accuracy metrics
def calculate_accuracy_metrics(y_true, y_pred):
    """
    Calculate multiple accuracy metrics for model evaluation
    """
    mape = mean_absolute_percentage_error(y_true, y_pred) * 100
    accuracy = 100 - mape  # Convert MAPE to accuracy percentage
    
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = np.mean(np.abs(y_true - y_pred))
    
    # Calculate percentage of predictions within different error margins
    errors = np.abs((y_true - y_pred) / y_true) * 100
    within_5_percent = np.mean(errors <= 5) * 100
    within_10_percent = np.mean(errors <= 10) * 100
    within_20_percent = np.mean(errors <= 20) * 100
    
    return {
        'Accuracy (100-MAPE)': accuracy,
        'MAPE': mape,
        'RMSE': rmse,
        'MAE': mae,
        'Within 5% Error': within_5_percent,
        'Within 10% Error': within_10_percent,
        'Within 20% Error': within_20_percent
    }

# Train Random Forest models with accuracy testing
def train_rf_models(X, y):
    models = {}
    scores = {}
    feature_importance = {}
    accuracy_metrics = {}
    
    for metric in y.columns:
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y[metric], 
                                                           test_size=0.2, 
                                                           random_state=42)
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model
        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        rf.fit(X_train_scaled, y_train)
        
        # Make predictions
        y_pred = rf.predict(X_test_scaled)
        
        # Calculate accuracy metrics
        accuracy_metrics[metric] = calculate_accuracy_metrics(y_test, y_pred)
        
        # Store other results
        models[metric] = rf
        scores[metric] = {
            'R2': r2_score(y_test, y_pred),
            'RMSE': np.sqrt(mean_squared_error(y_test, y_pred)),
            'CV_Score': np.mean(cross_val_score(rf, X_train_scaled, y_train, cv=5))
        }
        feature_importance[metric] = pd.Series(rf.feature_importances_, 
                                             index=X.columns)
    
    return models, scores, feature_importance, accuracy_metrics

# Visualize results including accuracy metrics
def plot_results(feature_importance, scores, accuracy_metrics):
    # Feature importance plot
    plt.figure(figsize=(12, 6))
    importance_df = pd.DataFrame(feature_importance)
    sns.heatmap(importance_df, annot=True, cmap='YlOrRd', fmt='.3f')
    plt.title('Feature Importance Across Performance Metrics')
    plt.tight_layout()
    plt.show()
    
    # Model performance plot
    plt.figure(figsize=(10, 5))
    scores_df = pd.DataFrame(scores).T
    scores_df[['R2', 'CV_Score']].plot(kind='bar')
    plt.title('Model Performance Metrics')
    plt.ylabel('Score')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
    # Accuracy metrics plot
    plt.figure(figsize=(12, 6))
    accuracy_df = pd.DataFrame(accuracy_metrics).T
    accuracy_df[['Within 5% Error', 'Within 10% Error', 'Within 20% Error']].plot(kind='bar')
    plt.title('Prediction Accuracy Ranges')
    plt.ylabel('Percentage of Predictions')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Main analysis
def main():
    # Read data
    df = pd.read_csv('E:/ML Learning/NCKH/dummy_financial_data.csv')
    
    # Prepare data
    X, y = prepare_data(df)
    
    # Train models and get results
    models, scores, feature_importance, accuracy_metrics = train_rf_models(X, y)
    
    # Plot results
    plot_results(feature_importance, scores, accuracy_metrics)
    
    # Print detailed results
    print("\nModel Performance Scores:")
    print(pd.DataFrame(scores).round(3))
    
    print("\nAccuracy Metrics:")
    accuracy_df = pd.DataFrame(accuracy_metrics).round(2)
    print(accuracy_df)
    
    # Calculate and print average accuracy across all metrics
    avg_accuracy = np.mean([metrics['Accuracy (100-MAPE)'] for metrics in accuracy_metrics.values()])
    print(f"\nOverall Average Model Accuracy: {avg_accuracy:.2f}%")
    
    # Print detailed accuracy breakdown
    print("\nDetailed Accuracy Breakdown by Performance Metric:")
    for metric, metrics in accuracy_metrics.items():
        print(f"\n{metric}:")
        print(f"  Base Accuracy (100-MAPE): {metrics['Accuracy (100-MAPE)']:.2f}%")
        print(f"  Predictions within 5% error: {metrics['Within 5% Error']:.2f}%")
        print(f"  Predictions within 10% error: {metrics['Within 10% Error']:.2f}%")
        print(f"  Predictions within 20% error: {metrics['Within 20% Error']:.2f}%")
    
    return models, scores, feature_importance, accuracy_metrics

if __name__ == "__main__":
    models, scores, feature_importance, accuracy_metrics = main()