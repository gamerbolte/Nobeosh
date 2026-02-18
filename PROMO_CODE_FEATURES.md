# Promo Code Features - Test Guide

## ✅ Implemented Features

### 1. Login Required to Use Promo Codes
- ✅ Customers MUST be logged in to apply promo codes
- ✅ Works on both Checkout Page and Product Page
- ✅ Error message shown if not logged in: "Please login to use promo codes"

### 2. Max Uses Per Customer
- ✅ Admin can set how many times each customer can use a promo code
- ✅ Tracked per customer email address
- ✅ Usage is recorded in `promo_usage` collection when order is placed

---

## 🧪 Testing Instructions

### Test 1: Login Requirement
1. Go to any product page or checkout
2. Try to apply a promo code WITHOUT logging in
3. Expected: Error message "Please login to use promo codes"

### Test 2: Max Uses Per Customer
1. **Create a promo code:**
   - Login to admin panel: `/panelgsnadminbackend/login`
   - Go to Marketing → Promo Codes
   - Create new promo code:
     - Code: `WELCOME10`
     - Discount: 10% off
     - Max Uses: 100 (total)
     - **Max Uses Per User: 2** ← This is the new feature!
   
2. **Test the limit:**
   - Login as a customer
   - Place first order with `WELCOME10` → Success ✅
   - Place second order with `WELCOME10` → Success ✅
   - Try third order with `WELCOME10` → Error: "You have reached the maximum 2 uses for this promo code" ❌

### Test 3: Different Customers Can Use Same Code
1. Customer A uses `WELCOME10` twice (reaches limit)
2. Customer B can still use `WELCOME10` (separate limit)
3. Each customer has their own usage counter

---

## 📊 Database Structure

### Promo Code Document
```json
{
  "id": "uuid",
  "code": "WELCOME10",
  "discount_type": "percentage",
  "discount_value": 10,
  "max_uses": 100,
  "max_uses_per_customer": 2,  ← Per-customer limit
  "used_count": 15,  ← Total uses across all customers
  "is_active": true
}
```

### Promo Usage Tracking
```json
{
  "id": "uuid",
  "promo_code": "WELCOME10",
  "order_id": "order-uuid",
  "customer_email": "customer@example.com",
  "used_at": "2026-02-18T16:30:00Z"
}
```

---

## 🔧 Admin Panel Guide

### Setting Max Uses Per Customer

1. Go to: **Marketing → Promo Codes**
2. Click "Add Promo Code" or edit existing
3. Find field: **"Max Uses Per User"**
4. Enter number (e.g., `2` for 2 uses per customer)
5. Leave blank for unlimited uses per customer
6. Save

**Field Description:**
> Limit how many times each logged-in user can use this code

---

## 🎯 Use Cases

### Use Case 1: Welcome Bonus
```
Code: WELCOME10
Discount: 10% off
Max Uses: 1000 (total)
Max Uses Per User: 1 (one-time only per customer)
```
Perfect for new customer welcome discounts.

### Use Case 2: Loyalty Reward
```
Code: LOYAL20
Discount: 20% off
Max Uses: Unlimited
Max Uses Per User: 5 (can use 5 times)
```
Reward loyal customers with multiple uses.

### Use Case 3: Limited Campaign
```
Code: FLASH50
Discount: 50% off
Max Uses: 100 (first 100 orders)
Max Uses Per User: 2 (each customer can buy twice)
```
Flash sale with per-customer limits.

---

## 🔒 Security & Validation

### Checks Performed (in order):

1. ✅ **Customer logged in?** 
   - If no → Error: "Please login to use promo codes"

2. ✅ **Code valid and active?**
   - If no → Error: "Invalid or expired promo code"

3. ✅ **Not expired?**
   - If expired → Error: "Promo code has expired"

4. ✅ **Minimum order met?**
   - If not met → Error: "Minimum order amount is Rs X"

5. ✅ **Global uses not exceeded?**
   - If exceeded → Error: "Promo code has reached maximum uses"

6. ✅ **Customer uses not exceeded?** ← NEW!
   - If exceeded → Error: "You have reached the maximum X uses for this promo code"

7. ✅ **First-time buyer restriction?**
   - If not first order → Error: "This promo code is only for first-time buyers"

8. ✅ **Category/Product restrictions?**
   - If not applicable → Error: "This promo code is not applicable to items in your cart"

---

## 📝 API Endpoints

### Validate Promo Code
```bash
POST /api/promo-codes/validate?code=WELCOME10&subtotal=1000&customer_email=user@example.com
```

**Response (Success):**
```json
{
  "valid": true,
  "code": "WELCOME10",
  "discount_amount": 100.0,
  "discount_type": "percentage",
  "discount_value": 10.0
}
```

**Response (Max Uses Exceeded):**
```json
{
  "detail": "You have reached the maximum 2 uses for this promo code"
}
```

### Create Promo Code (Admin)
```bash
POST /api/promo-codes
Authorization: Bearer <admin_token>

{
  "code": "WELCOME10",
  "discount_type": "percentage",
  "discount_value": 10,
  "max_uses": 100,
  "max_uses_per_customer": 2,
  "is_active": true
}
```

---

## 🎨 Frontend Changes

### Checkout Page (`CheckoutPage.jsx`)
- ✅ Validates customer is logged in before allowing promo code
- ✅ Passes customer email to validation endpoint
- ✅ Sends promo code to backend when creating order

### Product Page (`ProductPage.jsx`)
- ✅ Validates customer is logged in before allowing promo code
- ✅ Passes customer email to validation endpoint
- ✅ Sends promo code to backend when creating order

### Admin Promo Codes (`AdminPromoCodes.jsx`)
- ✅ Shows "Max Uses Per User" field in create/edit form
- ✅ Displays per-user limit in promo code list
- ✅ Help text explains the feature

---

## 🚀 Quick Test Commands

### Test without login (should fail):
```bash
curl -X POST "http://localhost:8001/api/promo-codes/validate?code=WELCOME10&subtotal=1000"
# Expected: {"detail": "Please login to use promo codes"}
```

### Test with login (should succeed):
```bash
curl -X POST "http://localhost:8001/api/promo-codes/validate?code=WELCOME10&subtotal=1000&customer_email=test@example.com"
# Expected: {"valid": true, "discount_amount": 100.0, ...}
```

### Check promo usage count:
```bash
# Login to MongoDB
mongo gameshop_nepal

# Check usage for a customer
db.promo_usage.count({
  "promo_code": "WELCOME10",
  "customer_email": "test@example.com"
})
```

---

## ✅ Summary

**What Changed:**
1. ✅ Promo codes now require customer login (both frontend validation and backend enforcement)
2. ✅ Admin can set `max_uses_per_customer` field
3. ✅ Backend tracks promo usage per customer in `promo_usage` collection
4. ✅ Validation checks customer usage count before allowing promo code
5. ✅ Order creation records promo usage automatically

**User Experience:**
- Customers must login to use any promo code
- Clear error messages guide the user
- Usage limits prevent abuse
- Each customer has independent usage tracking

**Admin Control:**
- Full control over per-customer limits
- Can create unlimited, one-time, or multi-use promo codes
- Usage statistics tracked in database

---

Last Updated: February 18, 2026
