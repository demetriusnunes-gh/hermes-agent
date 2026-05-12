# Recent false-positive guards

- **Gmail delivery failures** like `Mail Delivery Subsystem` / `Delivery Status Notification (Failure)` are usually **not** relevant by themselves.
  - Only flag if the body clearly ties the bounce to a specific real order, invoice, or family/priority message that needs attention.
- **Body keywords alone are not enough** when the sender is clearly a newsletter, promo, or automated marketing source.
- For school-related mail, prefer senders/subjects that clearly indicate the school itself or an actual school communication; incidental mentions of `Eleva` inside newsletters should stay unflagged.
