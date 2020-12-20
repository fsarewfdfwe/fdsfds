import discord
import asyncio
import os
from discord.ext import commands
import urllib
from urllib.request import URLError
from urllib.request import HTTPError
from urllib.request import urlopen
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from urllib.parse import quote
import re # Regex for youtube link
import warnings
import requests
import time


client = discord.Client() # Create Instance of Client. This Client is discord server's connection to Discord Room
token_path = os.path.dirname( os.path.abspath( __file__ ) )+"/token.txt"
t = open(token_path,"r",encoding="utf-8")
token = t.read().split()[0]
print("Token_key : ",token)


@client.event # Use these decorator to register an event.
async def on_ready(): # on_ready() event : when the bot has finised logging in and setting things up
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Type !help or !도움말 for help"))
    print("New log in as {0.user}".format(client))

@client.event
async def on_message(message): # on_message() event : when the bot has recieved a message
    #To user who sent message
    # await message.author.send(msg)
    print(message.content)
    if message.author == client.user:
        return

    if message.content.startswith("c!코로나"):
        # 보건복지부 코로나 바이러스 정보사이트"
        covidSite = "http://ncov.mohw.go.kr/index.jsp"
        covidNotice = "http://ncov.mohw.go.kr"
        html = urlopen(covidSite)
        bs = BeautifulSoup(html, 'html.parser')
        latestupdateTime = bs.find('span', {'class': "livedate"}).text.split(',')[0][1:].split('.')
        statisticalNumbers = bs.findAll('span', {'class': 'num'})
        beforedayNumbers = bs.findAll('span', {'class': 'before'})

        #주요 브리핑 및 뉴스링크
        briefTasks = []
        mainbrief = bs.findAll('a',{'href' : re.compile('\/tcmBoardView\.do\?contSeq=[0-9]*')})
        for brf in mainbrief:
            container = []
            container.append(brf.text)
            container.append(covidNotice + brf['href'])
            briefTasks.append(container)
        print(briefTasks)

        # 통계수치
        statNum = []
        # 전일대비 수치
        beforeNum = []
        for num in range(7):
            statNum.append(statisticalNumbers[num].text)
        for num in range(4):
            beforeNum.append(beforedayNumbers[num].text.split('(')[-1].split(')')[0])

        totalPeopletoInt = statNum[0].split(')')[-1].split(',')
        tpInt = ''.join(totalPeopletoInt)
        lethatRate = round((int(statNum[3]) / int(tpInt)) * 100, 2)
        embed = discord.Embed(title="코로나바이러스 한국 통계", description="",color=0x5CD1E5)
        embed.add_field(name="자료출처 : 보건복지부", value="http://ncov.mohw.go.kr/index.jsp", inline=False)
        embed.add_field(name="최근 업데이트 시간",value="해당 자료는 " + latestupdateTime[0] + "월 " + latestupdateTime[1] + "일 "+latestupdateTime[2] +" 자료입니다.", inline=False)
        embed.add_field(name="확진환자(누적)", value=statNum[0].split(')')[-1]+"("+beforeNum[0]+")",inline=True)
        embed.add_field(name="완치환자(격리해제)", value=statNum[1] + "(" + beforeNum[1] + ")", inline=True)
        embed.add_field(name="치료중(격리 중)", value=statNum[2] + "(" + beforeNum[2] + ")", inline=True)
        embed.add_field(name="사망", value=statNum[3] + "(" + beforeNum[3] + ")", inline=True)
        embed.add_field(name="누적확진률", value=statNum[6], inline=True)
        embed.add_field(name="치사율", value=str(lethatRate) + " %",inline=True)
        embed.add_field(name="- 최신 브리핑 1 : " + briefTasks[0][0],value="Link : " + briefTasks[0][1],inline=False)
        embed.add_field(name="- 최신 브리핑 2 : " + briefTasks[1][0], value="Link : " + briefTasks[1][1], inline=False)
        embed.set_thumbnail(url="https://wikis.krsocsci.org/images/7/79/%EB%8C%80%ED%95%9C%EC%99%95%EA%B5%AD_%ED%83%9C%EA%B7%B9%EA%B8%B0.jpg")
        embed.set_footer(text='코로나바이러스 알림이',
                         icon_url='https://raw.githubusercontent.com/fsarewfdfwe/fg/main/unnamed.png?token=ARK2I5R4G4I63OYVTNFLYGK7UYYXY')
        await message.channel.send("**Covid-19**코로나바이러스 한국 통계", embed=embed)

    if message.content.startswith("!봇 초대"):
        embed=discord.Embed(title = '봇초대', url = "https://discord.com/api/oauth2/authorize?client_id=754196852403863593&permissions=2081418487&redirect_uri=https%3A%2F%2Fwww.integromat.com%2Fscenario%2F1713463%2Fedit&scope=bot", description= "봇을 초대 한다.")
        await message.author.send(embed=embed)


    if str(message.content).split('`')[3]==None:
      if message.author.id == 700298171745697804:
        return await message.send(f'{message.author.mention}, 메시지를 적어주세요!')
    else:
        em = discord.Embed(title="봇이름", description=(f'{message.content}\n───────────────────────────'), colour=message.author.color)
        em.add_field(name='공지가 다른 채널로 왔으면 좋을거같나요?', value='그럼 ``봇공지``채널을 만들어주세요!')
        em.set_footer(text=f'공지 작성자: {message.author} - 개발자', icon_url=message.author.avatar_url)

        for ch in client.guilds:
            chid = [0]
            sendsuc = 0
            allow = False
            flag = True
            z = 0
            for ch2 in ch.channels:
                chid.append(ch2.id)
                z += 1
                if "봇공지" in ch2.name:
                    if str(ch2.type) == 'text':
                        try:
                            sendsuc += 1
                            await ch2.send(embed=em)
                            allow = True
                        except:
                            pass
                        break
            if allow == False:
                chan = ch.channels[1]

                if str(chan.type) == 'text':
                    try:
                        sendsuc += 1
                        await chan.send(embed=em)
                    except:
                        pass
        succ = discord.Embed(title='공지발신성공', description=f'{len(client.guilds)}개의 서버 중 {sendsuc}개의 서버에 발신 완료, {len(client.guilds)}개의 서버에 발신 실패', colour=message.author.color)
        await message.channel.send(embed=succ)


client.run(token)
