# 📌 Lab – Query Optimization and Execution Plan

## 📖 Purpose

The goal of this lab is to understand how SQL queries are processed and to identify why some queries execute faster than others.

The focus is on:
- query optimization techniques
- execution plan generation
- cost-based decision making

---

## 🎯 Objectives

By completing this lab, you should be able to:

- Understand, compare, and implement **query optimization transformation rules**
- Identify trade-offs between different optimization techniques
- Distinguish between:
  - **transactional workloads (OLTP)**
  - **analytical workloads (OLAP)**
- Interpret and critically analyze **database system architectures**
- Understand how **cost estimation** influences execution plans

---

## ⚙️ General Requirements

- You may use **any programming language**
- You are NOT required to implement a full SQL parser
- You may represent queries internally using:
  - objects
  - structures (e.g., tables, joins, conditions)

---

## 🧱 Data Model Requirements

The system must include:

- ✅ At least **5 tables**
- ✅ At least **3 indexes**, including:
  - at least **one composite (multi-column) index**

---

## 🧩 Query Representation

Instead of parsing raw SQL, you can model queries using objects such as:

- `Table`
- `Join`
- `WhereClause`
- `Condition`
- `Index`
