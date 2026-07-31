# The Olive Table — Bot Messages (English + Arabic)

Restaurant reservation bot messages for all states, nudges, and handoff, in both English and Arabic. The bot detects the language of the user's message and always replies in that same language, switching automatically if the user switches mid-conversation.

---

## State 1: Greeting + Intent

**English:**
```
Welcome to The Olive Table! 🌿
Would you like to make a reservation, or do you have a question?
1. Make a reservation
2. Ask a question
```

**Arabic:**
```
مرحباً بك في ذا أوليف تيبل! 🌿
هل ترغب في حجز طاولة، أم لديك سؤال؟
1. حجز طاولة
2. لدي سؤال
```

---

## State 2: Ask Service

**English:**
```
Great! What would you like to book?
1. Lunch table
2. Dinner table
3. Special occasion (birthday, celebration, etc.)
```

**Arabic:**
```
رائع! ماذا تودّ أن تحجز؟
1. طاولة غداء
2. طاولة عشاء
3. مناسبة خاصة (عيد ميلاد، احتفال، إلخ)
```

---

## State 3: Ask Timing

**English:**
```
Perfect. What date and time would you like to book for?
(e.g., "Tomorrow at 7 PM" or "Friday at 1 PM")
```

**Arabic:**
```
ممتاز! ما هو التاريخ والوقت الذي تفضله؟
(مثال: "غدًا الساعة 7 مساءً" أو "الجمعة الساعة 1 ظهرًا")
```

---

## State 4: Offer Slots

> Note: these are mock/example slots for Phase 1. In a real deployment, this list would be pulled dynamically from a connected calendar (Phase 2), not hardcoded.

**English:**
```
Here are the available slots near your requested time:
1. Friday, 7:00 PM
2. Friday, 7:30 PM
3. Friday, 8:00 PM
Which one works for you?
```

**Arabic:**
```
إليك الأوقات المتاحة القريبة من الوقت الذي طلبته:
1. الجمعة، 7:00 مساءً
2. الجمعة، 7:30 مساءً
3. الجمعة، 8:00 مساءً
ما هو الوقت المناسب لك؟
```

---

## State 5: Confirm Booking

**English:**
```
You're all set! ✅
Reservation confirmed for The Olive Table:
📅 Friday, 7:30 PM
🍽️ Dinner table
We look forward to seeing you! Reply anytime if you need to change or cancel your booking.
```

**Arabic:**
```
تم كل شيء! ✅
تم تأكيد حجزك في ذا أوليف تيبل:
📅 الجمعة، الساعة 7:30 مساءً
🍽️ طاولة عشاء
نتطلع لرؤيتك! راسلنا في أي وقت إذا أردت تعديل أو إلغاء الحجز.
```

---

## No-Reply Nudges

> Important: only the **+1h nudge** is a free-form message, allowed within WhatsApp's 24-hour customer service window. The **+24h and +72h nudges must be pre-approved template messages** in a real deployment — WhatsApp does not allow businesses to freely message a customer after 24 hours of inactivity without one. Meta template approval is not required for this phase, just noted here for the real build.

### Nudge 1 (+1 hour — free-form)

**English:**
```
Hi! Just checking in 🙂 Would you still like to book a table at The Olive Table? I'm here whenever you're ready.
```

**Arabic:**
```
مرحباً! أردنا فقط الاطمئنان عليك 🙂 هل ما زلت ترغب في حجز طاولة في ذا أوليف تيبل؟ نحن هنا عندما تكون جاهزًا.
```

### Nudge 2 (+24 hours — requires template approval)

**English:**
```
We noticed you started a reservation at The Olive Table. Would you like to continue booking your table?
```

**Arabic:**
```
لاحظنا أنك بدأت بحجز طاولة في ذا أوليف تيبل. هل ترغب في إكمال عملية الحجز؟
```

### Nudge 3 (+72 hours — requires template approval)

**English:**
```
Last check-in from The Olive Table 🌿 If you'd still like to book, just reply anytime and we'll pick up where we left off.
```

**Arabic:**
```
آخر تذكير من ذا أوليف تيبل 🌿 إذا كنت لا تزال ترغب في الحجز، فقط راسلنا في أي وقت وسنكمل من حيث توقفنا.
```

If there's still no response after the +72h nudge, the lead is marked as **lost**.

---

## Human Handoff

> Triggered by: any medical/health-related question, a complaint, a pricing negotiation, or anything off-script. The bot never improvises in these cases — it escalates immediately.

**English:**
```
That's a great question for our team directly — let me connect you with someone from The Olive Table who can help you right away. 🙋
```

**Arabic:**
```
هذا سؤال من الأفضل أن يجيب عليه فريقنا مباشرة — سأقوم بتوصيلك بأحد أعضاء فريق ذا أوليف تيبل ليساعدك فورًا. 🙋
```
