# Connecting Prometheus, PostgreSQL, and VictoriaMetrics with Grafana

---

## Step 1: Use Grafana for Visualization

Since VictoriaMetrics does not have a native UI, we will use **Grafana** for visualization.

---

## Step 2: Open Grafana and Login

- Access Grafana through your browser:
  
  ```
  http://localhost:3000
  ```
- Use the provided default credentials (Username: `admin`, Password: `admin`).

---

## Step 3: Configure Data Source

- On the Grafana home page, navigate to **"Data Sources"**.
- Select **Prometheus** as the data source (VictoriaMetrics option is not directly available).

---

## Step 4: Set the Data Source URL

- In the URL field, enter:

  ```
  http://localhost:8428/prometheus
  ```
- This URL will allow Grafana to POST the scraped data from Prometheus to VictoriaMetrics.

---

## Step 5: Save and Test the Connection

- Click on **Save & Test** to verify the connection.

---

## Step 6: Import a Dashboard

- Go to the **"+"** icon on the left side.
- Click on **"Import"**.

---

## Step 7: Load Dashboard by ID

- Enter the **Dashboard ID: 9628**.
- Click **Load**.

---

## Step 8: Set the Correct Data Source

- In the dropdown, select the data source ending with `/prometheus`.
- This ensures correct linkage between Grafana and VictoriaMetrics via Prometheus.
