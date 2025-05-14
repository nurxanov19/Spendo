# Spendo 

# Bu loyiha Xarajatlaringiz va daromadlaringizni kuzatib borishingizda sizga yuqori sifatdagi zamonaviy funksionallikni ta'mminlab beradi.

#AuthOneView
-- foydalanuvchi email yoki telefon raqam yuborad
-- tasodifiy 6 xonali kod (OTP) yaratiladi
-- fodalanuvchi rostdan ham shu telefon/email egasi ekanligini aniqlash maqsadida kod yuboradi

#AuthTwoView
-- foydalanuvchi oldin yuborilgan key va OTP kodni kiritadi
-- tizi esa ushbu key borligini tekshiradi. OTP kod to‘g‘ri ekanini tekshiradi (so‘nggi 6 xonasi). Urinishlar soni 3 tadan oshmaganligini tekshiradi
-- Agar hammasi joyida bo‘lsa: is_confirmed = True
-- Maqsadi: bu phone/email rostdan ham foydalanuvchiga tegishli ekanligi tasdiqlanadi
