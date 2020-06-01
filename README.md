# Discord-Auction-Bot

Discord bot for creating auctions.

You can add your server from this link.
https://top.gg/bot/702203935506563082

______________________________________________________
Tr:

Discord'ta müzayede oluşturmanızı sağlayan botun kaynak kodları.

Öncelikle oluşturulan müzayedeler her hangi bir veritabanında tutulmamaktadır. Her bir müzayede discord mesajı oldugundan bu mesajların ID si kullanılarak işlem yapılmıştır.

Kullanılan kütüphaneler:

*Discord
*Time
*datetime
*pytimeparse
*asyncio
*validator

________________________________________________

Kısaca çalışma mantığı:


Bir müzayede oluşturduğunuzda , oluşturduğunuz andan itibaren asekron bir metod çalışır ve sizin verdiğiniz süre doluncaya kadar müzayede açık kalır.Aynı zamanda asekron görev kuyruğuna eklenir.
Müzayede açık olduğu sürece herkes teklif verebilir.
Süre dolduğunda kazanan ekrana yazdırılır.
