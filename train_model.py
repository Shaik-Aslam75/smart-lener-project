import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load Dataset
df = pd.read_csv("loan_prediction.xlsx.csv")

# Drop Loan_ID
df.drop("Loan_ID", axis=1, inplace=True)

# Fill Missing Values
df = df.ffill()

# Encode ONLY categorical columns
df["Gender"] = df["Gender"].map({"Male":1,"Female":0})
df["Married"] = df["Married"].map({"Yes":1,"No":0})
df["Education"] = df["Education"].map({"Graduate":1,"Not Graduate":0})
df["Self_Employed"] = df["Self_Employed"].map({"Yes":1,"No":0})
df["Property_Area"] = df["Property_Area"].map({
    "Rural":0,
    "Semiurban":1,
    "Urban":2
})
df["Loan_Status"] = df["Loan_Status"].map({"N":0,"Y":1})
df["Dependents"] = df["Dependents"].replace("3+",3).astype(int)

# Features
X = df.drop("Loan_Status", axis=1)
y = df["Loan_Status"]

# Train
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

joblib.dump(model, "model.pkl")

print("✅ Model Created Successfully")