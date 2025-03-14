# **RevoBank Activity Diagrams _(User Authentication and Transaction Handling)_**

## **Introduction**

This repository contains two **UML Activity Diagrams** for RevoBank:

1. **User Authentication Process**
2. **Transaction Handling Process**

Both diagrams describe the workflows involved in authenticating users and handling various types of transactions in a system.

---

## **1. User Authentication Activity Diagram**

### **Purpose:**

The User Authentication Activity Diagram illustrates the steps involved in authenticating a user, from login to error handling and token generation.

### **Steps:**

1. **User Login:**
   - **Action:** User enters their username and password.
2. **Password Verification:**
   - **Action:** Authentication Service verifies the credentials.
   - **Decision:** Are the credentials valid?
     - **Yes:** Proceed to Token Generation.
     - **No:** Return to "User Login" with an error message.
3. **Error Handling:**
   - **Action:** Display error message to the user.
   - **Decision:** Does the user retry the login?
     - **Yes:** Go back to "User Login."
     - **No:** End the process.
4. **Token Generation:**
   - **Action:** Authentication Service generates a session token.
   - **Outcome:** User is granted access with the token.

---

## **2. Transaction Handling Activity Diagram**

### **Purpose:**

The Transaction Handling Activity Diagram details the steps involved in initiating and processing a transaction, including actions like checking balance, transferring funds, instant payments, and top-ups for e-wallets.

### **Steps:**

#### **Initiate Transaction:**

- **Action:** User chooses a transaction type (e.g., check balance, transfer, instant payment, top-up e-wallet).

#### **Select Transaction Type:**

**Action:** User selects a transaction option:

1. **Check Balance**

   - **Action:** User selects "Check Balance."
   - **Transaction Service:** Queries the banking system for the current account balance.
   - **Outcome:** The system displays the current balance to the user.
   - **Decision:** Does the user wish to proceed with another transaction?
     - **Yes:** Go back to "Select Transaction Type."
     - **No:** End the process.

2. **Transfer:**

   - **Action:** User selects "Transfer" and enters transfer details (recipient account, amount).
   - **Transaction Service:** Verifies account balance for sufficient funds.
   - **Decision:** Is the balance sufficient for the transfer?
     - **Yes:** Proceed to transfer.
     - **No:** Display error (insufficient funds).
   - **Action:** Transfer funds if balance is sufficient.
   - **Outcome:** Transaction completes, and both sender and recipient receive confirmation.
   - **Action:** Generate transaction history.
     - **Outcome:** Transaction details are added to the user's history.
   - **Decision:** Does the user wish to proceed with another transaction?
     - **Yes:** Go back to "Select Transaction Type."
     - **No:** End the process.

3. **Top-up E-wallet:**

   - **Action:** User selects "Top-up E-wallet" and enters e-wallet details (amount to top up).
   - **Transaction Service:** Verifies account balance for sufficient funds.
   - **Decision:** Is the balance sufficient for the top-up?
     - **Yes:** Proceed with top-up process.
     - **No:** Display error (insufficient funds).
   - **Action:** Top-up the user’s e-wallet balance if sufficient funds are available.
   - **Outcome:** E-wallet balance is updated.
   - **Action:** Generate transaction history.
     - **Outcome:** Transaction details are added to history.
   - **Decision:** Does the user wish to proceed with another transaction?
     - **Yes:** Go back to "Select Transaction Type."
     - **No:** End the process.

4. **Instant Payment:**

   - **Action:** User selects "Instant Payment" and enters payment details (payee, amount).
   - **Transaction Service:** Verifies account balance for sufficient funds.
   - **Decision:** Is the balance sufficient for the payment?
   - **Yes:** Proceed to payment processing.
   - **No:** Display error (insufficient funds).
   - **Action:** Complete the payment immediately if funds are sufficient.
   - **Outcome:** Instant payment is confirmed and a receipt is generated.
   - **Action:** Generate transaction history.
   - **Outcome:** Transaction details are updated in history.
   - **Decision:** Does the user wish to proceed with another transaction?
   - **Yes:** Go back to "Select Transaction Type."
   - **No:** End the process.

**End Transaction:**

- **Outcome:** After completing a transaction or if an error occurs, the user can either exit the process or retry.

---

## **Key Decisions and Processes**

### **User Authentication Diagram:**

- **Decision 1:** Valid credentials (success) vs. Invalid credentials (failure).
- **Decision 2:** Retry the login or exit on failure.
- **Action:** Successful login generates a token, granting access to the user.

### **Transaction Handling Diagram:**

- **Balance Check:** Before processing any transaction, the system verifies if the user has sufficient funds.
- **Transaction Type Selection:** The user can select from various transaction options like **Check Balance**, **Transfer**, **Instant Payment**, and **Top-up E-wallet**.
- **Transaction Completion:** If the transaction is successful, the user's transaction history is updated.
- **Error Handling:** If the balance is insufficient or an error occurs, the user can retry or cancel the operation.

---

## **Conclusion**

These activity diagrams capture the key workflows in **User Authentication** and **Transaction Handling**. They provide a clear visual representation of how users interact with the system to authenticate and perform various types of transactions. The diagrams are designed to help stakeholders understand the process flow, decisions, and actions involved in each workflow.

## License

Used for submission Assignment Project Milestone 3, RevoU FSSE Program.

---

© 2025 Activity Diagrams of RevoBank. All Rights Reserved. Created by @anggreinipra
