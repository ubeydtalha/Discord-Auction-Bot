import discord
import discord.guild
import sched,time
from datetime import datetime,timedelta
from pytimeparse.timeparse import timeparse
import asyncio
from discord.ext import commands
from discord.embeds import EmbedProxy
import validators


TOKEN = '
'
#client = discord.Client()
messages = 0
kontrol = bool()


bot = commands.Bot(command_prefix= '$')

#id = bot.get_guild(669662960561553428)


@bot.event
async def on_ready():

    print(f'Logged in as: {bot.user.name}')
    print(f'With ID: {bot.user.id}')


@bot.command()
async def ping(ctx):
    await ctx.send('pong')




class item():
    name = "default" #itemın adı
    feature = "" #itemın özellikleri
    #price = 0 #müzayede dışında satış fiyatı
    Price = None #müzayede başlangıç fiyatı
    timer = ""  #
    
    def __init__(self,name,feature,Price,timer):
        super().__init__()
        self.name = name
        self.feature = feature
        self.Price = Price
        self.timer = timer

class muzayede():
    mid = 0
    item = item("","",None,"")
    createdDate = datetime.now()
    leftTime = timedelta(0)
    currentTime = ""
    author = ""
    Winner = ""
    isFinished = False


    def __init__(self,item,createdDate,leftTime,author):
        super().__init__()
        self.item = item
        self.createdDate = createdDate
        self.leftTime = leftTime
        self.author = author
        
    
    def creatId(self,mid):
        self.mid = mid
          
                    
async def winner(win):
    return win

#%% Delete
@bot.command(pass_context=True)
async def delete(ctx,mid):
    channel = ctx.message.channel
    try:
        msg =await channel.fetch_message(mid)
        
        #print(ctx.message.author.name)
        #print(msg.embed[0].fields[4].value)
        if msg:
            await msg.delete()
        else:
            fail = await channel.send("Auction not found")
            await fail.delete(delay=10)   
        
    except Exception as e:
        fail = await channel.send("Please, Use command correctly or Auction not found! You can try $helpme")
        await fail.delete(delay=10)   

#%% Help
#    
@bot.command(pass_context=True)
async def helpme(ctx):
    channel = ctx.message.channel
    
    try:
        user = ctx.message.author
        msg = await channel.send(f"""{user.mention} I send help for you <3""")
        await msg.delete(delay=10)

        embed = discord.Embed( #embed mesajımız oluştu
            title = "Help",
            description = "",
            colour = discord.Colour.blue()
        )

        embed.add_field(name="Create auction",
        value="You can create auction easly! :\n\n $create |ITEM NAME|Item description|Price(only numbers)|Time|Image URL \n",
        inline=False)
        embed.add_field(name="Offer auction",
        value="You can offer auction like this : \n\n $offer AuctionID offer \n Note :You can offer active auction and higger price \n ",
        inline=True)
        embed.add_field(name="Deleting Auction",
        value="You can delete your active auction like this : \n\n $delete AuctionID \n",
        inline=True)
        embed.add_field(name="Find Auction",
        value="You can find auction on last 30 message like this : \n\n $find \n",
        inline=True)
        embed.add_field(name="Time",
        value="You can define time like this: \n\n 32m,2h32m,3d2h32mü1w3d2h32m,1w 3d 2h 32m,1 w 3 d 2 h 32 m,\n4:13,4:13:02,4:13:02.266,2:04:13:02.266,2 days, \n  4:13:02 (uptime format),2 days,  4:13:02.266,5hr34m56s,\n5 hours, 34 minutes, 56 seconds,5 hrs, 34 mins, 56 secs,2 days, 5 hours, 34 minutes,\n 56 seconds,1.2 m,1.2 min,1.2 mins,1.2 minute,1.2 minutes,172 hours,172 hr,172 h,\n172 hrs,172 hour,1.24 days,5 d,5 day,5 days5.6 wk \n 5.6 week,5.6 weeks",
        inline=True)
        #await bot.send_message(user, embed=embed)
        embed.set_footer(text='(BETA)Created by MAJIN#4884' )
        
        dm = await user.create_dm()
        await dm.send(embed=embed)

        


    except Exception as e:
        msg = await channel.send(f"""Some error ^-^ Try $helpme """)
        await msg.delete(delay=10)



#%% embed 

@bot.command(pass_context=True)
async def create(ctx):
    channel = ctx.message.channel #atılan mesaj
    try:
        taskk = list() #müzayedelirin sıraya alındığı liste
        
        text = ctx.message.content.split('|')
        message = ctx.message   
        if len(text)==5:
            newItem = item(text[1],text[2],int(text[3]),(text[4]))
            text.append(" ")
        elif len(text)==6:
            newItem = item(text[1],text[2],int(text[3]),(text[4]))
        else:
            notEnoughmsg =await channel.send("Please, Use command correctly!You can try $helpme")
            await notEnoughmsg.delete(delay=10)
            
            ###################
            # Burada user yanlış mesaj attığı için mesajı silmek gerekli
            # ##################    
            return

        mesDate = ctx.message.created_at
        leftTime = timedelta(seconds= timeparse(newItem.timer)) #Str->TimeDelta
        
        nmuzayede = muzayede(newItem,mesDate,leftTime,message.author.name) #yeni bir müzayede oluştur diyorum  
        

        embed = discord.Embed( #embed mesajımız oluştu
            title = nmuzayede.item.name,
            description = nmuzayede.item.feature,
            colour = discord.Colour.blue()
        )
        
        #user = discord.utils.get(ctx.message.server.members, name = 'MAJIN', discriminator = 4884)
        embed.set_footer(text='(BETA)Created by MAJIN#4884' )
        valid=validators.url(text[5])
        if valid:
            embed.set_image(url=text[5])
        else:
            urlFail = await channel.send("Your picture URL is not correct!! So your auction dosen't have picture.")
            await urlFail.delete(delay=10)
        # Kullanıcı mesajı silinmeli !!!

            

        embed.set_thumbnail(url="")
        embed.set_author(name=muzayede.author,
        icon_url="")
        embed.add_field(name="Price", value=str(nmuzayede.item.Price), inline=True)
        embed.add_field(name="Time Limit", value=nmuzayede.item.timer, inline=True)
        embed.add_field(name="Winner", value=None, inline=True)
        embed.add_field(name="Author",value="{}".format(ctx.message.author.mention),inline=False)
        

        msg = await channel.send(content=None, embed=embed)
        print(msg.id)
        nmuzayede.mid=msg.id#Müzayede id si belirleniyor
        embed.add_field(name="Id",value=nmuzayede.mid,inline=False)
        await msg.edit(embed=embed)

        taskk.append(asyncio.create_task(count(nmuzayede)))
            
        for i in taskk:
            await i
            msgMuzayede =await channel.fetch_message(nmuzayede.mid)
            newMSG = msgMuzayede
            await msgMuzayede.delete()
            newMSG.embeds[0].insert_field_at(4,name="FINISHED",value="See you later....",inline=False)
            
            newMSG.embeds[0].remove_field(5)
            await channel.send(embed=newMSG.embeds[0])
            #ne = embed.insert_field_at(2,name="FINISHED",value="The Winner :") 
                #embed.clear_fields()
            #nmuzayede.isFinished=True
            #await msg.edit(embed=ne)
    except ValueError :
        fail = await channel.send("Please, Use command correctly!You can try $helpme")
        await fail.delete(delay=10)
    except Exception as e:
        fail = await channel.send("AL KIRDIN KIRDIN!You can try $helpme")
        await fail.delete(delay=10)

@bot.command(pass_context=True)
async def offer(ctx,mid,value): 
    #
    # ctx : offer mesajının kendisi
    # value : teklif edilen değer
    # mid = Müzayede id si mesaja buradan erişiyorum
    # Önce offerın bulundu channela gidip
    # müzayede idsinden müzayedeye ulaşalım
    channel = ctx.message.channel
    try:
        msgMuzayede =await channel.fetch_message(mid)

    #Mesajımıza ulaştık buradan embed ettiğim price kısmını kullanalım
    #  
        fields = msgMuzayede.embeds
        embedMsg = fields[0]
        currentValue = embedMsg.fields[0].value

        if embedMsg.fields[3].name == "FINISHED":
        #alert = await channel.send("Its Finished")
        #kullanıcın mesajını silme özelliği eklenmeli
            m=await channel.send("It is finished!!!")
            await m.delete(delay=15)

        

        elif int(value) > int(currentValue):
            embedMsg.set_field_at(0,name="Price",value=value,inline=True)
            embedMsg.set_field_at(2,name="Winner",value=ctx.message.author.mention,inline=True)
            await msgMuzayede.edit(embed=embedMsg)



        else:
            delete = await channel.send("You should offer higher than {}".format(currentValue))
            await delete.delete(delay=20)
        #Gerekli izinler alınırsa düşük , gereksiz ve yanlış tekliflerde silinebilinir


    #await channel.send(f"""{embedMsg.fields[0].value}""")
    #print(type(embedMsg.fields[0]))
    #print(type(embedMsg.fields[0].add_fields))
        print(type(embedMsg))
    except Exception as e:
        await channel.send("This Id is unavailable You can try $helpme")
    

@bot.command(pass_context=True)
async def find(ctx):
    try:
        counter = 0
        channel = ctx.message.channel
        async for msg in channel.history(limit=30):
            for embeds in msg.embeds:
                if embeds.fields[3]:
                    #await channel.send(content=f"""{embeds.fields[3].name}""",embed=embeds)
                    if embeds.fields[3].name != "FINISHED":
                        await channel.send(embed=embeds)
                    else:
                         await channel.send("There is no opened trade")   
    
    except Exception as e:
        if e == "list index out of range":
            await channel.send("There is no trade more")
        else:
            await channel.send(e)


        
        
async def count(muzayede):
    mesDate = muzayede.createdDate
    leftTime = muzayede.leftTime
    fark = datetime.utcnow()- mesDate
    print(f'Counter')
    while(fark<=leftTime):
        #print(f'fark {fark}')
        suan = datetime.utcnow()
        fark = suan- mesDate
        muzayede.currentTime = str(fark)
        await asyncio.sleep(1)



bot.run(TOKEN)
