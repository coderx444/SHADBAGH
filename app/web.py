from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
import re
import random
import pandas as pd
import json
from typing import Dict, Any
from datetime import datetime
from fastapi.staticfiles import StaticFiles


session = requests.Session()


app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "is_active": is_active}
    )


@app.get("/index", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "is_active": is_active}
    )


@app.get("/disconnection", response_class=HTMLResponse)
async def disconnection(request: Request):
    return templates.TemplateResponse(
        "disconnection.html", {"request": request, "is_active": is_active}
    )


@app.get("/generate", response_class=HTMLResponse)
async def generate(request: Request):
    return templates.TemplateResponse(
        "generate.html", {"request": request, "is_active": is_active}
    )


@app.get("/duplications", response_class=HTMLResponse)
async def duplications(request: Request):
    return templates.TemplateResponse(
        "duplications.html", {"request": request, "is_active": is_active}
    )


def is_active(request: Request, link: str) -> str:
    return "active" if request.url.path == link else ""


# ----------------------------------------------------------------

# ##########################################################
# ######### OOOOO >------>> START <<------< OOOOO ##########
# ##########################################################


# load useragent
def read_user_agents(ua_path):
    with open(ua_path) as f:
        user_agents = [line.strip() for line in f]
        random.shuffle(user_agents)
        return user_agents


def generate_cookies(ua_lst):
    ua = random.choice(ua_lst)
    headers = {
        "User-Agent": ua,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://duplicatebill.wasa.punjab.gov.pk/",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
    }
    return {
        "ASP.NET_SessionId": requests.get(
            "https://duplicatebill.wasa.punjab.gov.pk/duplicate_bill.aspx",
            headers=headers,
        )
        .cookies.get_dict()
        .get("ASP.NET_SessionId"),
        "ua": ua,
    }


def hit_account(account_no, ua, cj):
    headers = {
        "User-Agent": ua,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://duplicatebill.wasa.punjab.gov.pk",
        "Connection": "keep-alive",
        "Referer": "https://duplicatebill.wasa.punjab.gov.pk/",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
    }
    data = {
        "ctl00_RadScriptManager1_HiddenField": ";;System.Web.Extensions, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35:en-US:14a9c2eb-bf69-4b0e-9aa0-eb85640f0e43:ea597d4b:b25378d2;;System.Web.Extensions, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35:en-US:14a9c2eb-bf69-4b0e-9aa0-eb85640f0e43:ea597d4b:b25378d2;;System.Web.Extensions, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35:en-US:14a9c2eb-bf69-4b0e-9aa0-eb85640f0e43:ea597d4b:b25378d2;;System.Web.Extensions, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35:en-US:14a9c2eb-bf69-4b0e-9aa0-eb85640f0e43:ea597d4b:b25378d2;;System.Web.Extensions, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35:en-US:14a9c2eb-bf69-4b0e-9aa0-eb85640f0e43:ea597d4b:b25378d2;;System.Web.Extensions, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35:en-US:14a9c2eb-bf69-4b0e-9aa0-eb85640f0e43:ea597d4b:b25378d2",
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "__VIEWSTATE": "/wEPDwUKMTEwOTMzODEzNQ9kFgJmD2QWAgIDD2QWAgIDDxQrAAIUKwACZBAWAWYWARQrAAJkZA8WAWYWAQVzVGVsZXJpay5XZWIuVUkuUmFkTWVudUl0ZW0sIFRlbGVyaWsuV2ViLlVJLCBWZXJzaW9uPTIwMDkuMi43MDEuMjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49MTIxZmFlNzgxNjViYTNkNGRkZLkKyPGUUd3klL8YLALzYNTQrcwCUeEm0d2BC4U53hZf",
        "__VIEWSTATEGENERATOR": "0FE07671",
        "__EVENTVALIDATION": "/wEdAASucRN5w6JLOrv1db0DL/X372z5nhRiYeIG8c5UtSGWyvghyNihoa4DpHvw24QeCw2DNehHWFObL9eLrwLxQAtjJCOCRrcyAnH9LAQtxS8IzkH6Ift9seqi7iQzVxnrF6Q=",
        "ctl00$MainContent$txtAccountNo": f"{account_no}",
        "ctl00$MainContent$btnSubmit": "Submit",
    }
    cookies = {
        "ASP.NET_SessionId": cj,
        "has_js": "1",
    }

    return requests.post(
        "https://duplicatebill.wasa.punjab.gov.pk/",
        cookies=cookies,
        headers=headers,
        data=data,
    )


def change_ua():
    global ua_lst, ua
    ua_lst.remove(ua)
    ua = random.choice(ua_lst)


# ============================= Regex Functionality


def cleaner(lsts):
    temp = " ".join([i for i in lsts if i != ""])
    return temp.replace("&nbsp;", " ")


def patterns_matches(tag, response):
    pattern = re.compile(f"{tag}.*?<span.*?>(.*?)<")
    return cleaner(pattern.findall(response.text))


def digits_ext(string):
    pattern = re.compile(r"(\d+)\.")
    return pattern.findall(string)[0]


def extract_info(res, cj, account_no):
    # data, cookies, url = generate_headers(account_no)
    # res = hit_account(account_no, data, cookies, url)

    info = {}

    pattern = re.compile(f"Sorry.*?!")
    not_found = pattern.findall(res.text)

    if not_found:
        return {
            "status": {"code": "error", "msg": "Record Not Found"},
            "session": {"ASP.NET_SessionId": cj},
            account_no: {},
        }

    else:
        # account_no = patterns_matches("AcNoACCTNUMR81", res).strip()
        name = patterns_matches("Name", res).strip()
        address = patterns_matches("ADDR", res).strip()
        ward = patterns_matches("WardNoWARDNUMR91", res).strip()
        # account_no = patterns_matches("AcNoACCTNUMR81", res).strip()
        property_no = patterns_matches("PropertyNoPPTYNUMR101", res).strip()
        type_ = patterns_matches("BILLSYSTDESCWH171", res).strip()
        connection = patterns_matches("ConnectionTypeCONDES361", res).strip()

        ammount_due_date = digits_ext(
            patterns_matches("AmountPayableRoundTCURDUES251", res)
        )

        ammount_after_date = digits_ext(
            patterns_matches("AmountPayableRoundTAMTAFDUE291", res)
        )
        demand = digits_ext(patterns_matches("TotalCurrentDemandTCURDMND231", res))
        arrears = digits_ext(patterns_matches("ArrearsBFTARERBF241", res))
        # raqba = patterns_matches("AreaAREAMRLA121", res).strip()
        # start = patterns_matches("BillingPeriodFromPERDSTRTD312", res).strip()
        # end = patterns_matches("BillingPeriodToPERDENDDA322", res).strip()
        # issue_date = patterns_matches("IssueDate131", res)
        # due_date = patterns_matches("DueDateCURRDUEDA161", res)

        if type_ == "AQUIFER":
            type_ = "Aquifer"
        else:
            type_ = "water_sewer"

        if connection == "DOMESTIC":
            connection = "domestic"
        else:
            connection = "commercial"

        info.update(
            {
                "status": {"code": "success", "msg": "Record Generated Sucessfully"},
                "session": {"ASP.NET_SessionId": cj},
                account_no: {
                    "consumer_name": name,
                    "visted_arears": address,
                    "ward_no": ward,
                    "account_no": account_no,
                    "property_no": property_no,
                    "type": type_,
                    "con": connection,
                    "bill_ammount": ammount_due_date.split(".")[0],
                    "ammount_after_date": ammount_after_date.split(".")[0],
                    "monthly_demand": demand.split(".")[0],
                    "arrears": arrears.split(".")[0],
                    # "raqba": raqba,
                    # "time_period": f"From {start} TO {end}",
                    # "issue_date": issue_date,
                    # "due_date": due_date,
                },
            }
        )
    return info


# ---------------------------------------------------------->
ua_path = "./ua.txt"

ua_lst = read_user_agents(ua_path)

# temp = generate_cookies(ua_lst)

cj = None
ua = None

counter = 1


@app.post("/process_data")
def process_data(data: Dict[Any, Any]):
    global ua_lst, ua, cj, counter

    data = json.dumps(data)
    data = json.loads(data)

    account_no = data.get("account_no")

    asp = data.get("ASP.NET_SessionId")

    if asp == "false" or counter >= 5:
        temp = generate_cookies(ua_lst)
        counter = 1

        cj = temp.get("ASP.NET_SessionId")
        ua = temp.get("ua")
        change_ua()

    else:
        cj = asp
        ua = random.choice(ua_lst)
        change_ua()

    if len(ua_lst) <= 50:
        ua_lst = read_user_agents(ua_path)

    counter += 1
    req = extract_info(hit_account(account_no, ua, cj), cj, account_no)

    import time

    time.sleep(6)
    return req


@app.post("/check_duplicates")
async def check_duplicates(request: Request):
    sheet_id = "1AH02FNm28gGE7jpLh3oBWE7kh7byhxeqSGCnORVjQ5A"
    gid = "931123515"

    df = pd.read_csv(
        f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?gid={gid}&format=csv"
    )

    data = await request.json()
    acc = []

    for k, v in data.items():
        acc.append(int(v["account_no"]))

    # acc duplicates accounts

    today_date = datetime.now().date()

    today_data = pd.DataFrame(data).T[["account_no", "bill_ammount", "paid"]]

    today_data["Date"] = f"{today_date.day}-{today_date.month}-{today_date.year}"
    date = pd.to_datetime(today_data["Date"], dayfirst=True)

    today_data["Day"] = date.dt.day_name().head(1).tolist()[0]
    today_data["Month"] = date.dt.month_name().head(1).tolist()[0]

    df = df[df["Account No"].isin(acc)].copy()

    today_data.rename(
        columns={
            "account_no": "Account No",
            "bill_ammount": "Bill Amount",
            "paid": "Paid",
        },
        inplace=True,
    )

    current = pd.concat([df, today_data])

    current["Account No"] = current["Account No"].astype(int)
    current["Date"] = pd.to_datetime(current["Date"], dayfirst=True)

    final = current.sort_values(by=["Account No", "Date"], ascending=[False, False])

    final["Date"] = final["Date"].dt.strftime("%d-%m-%Y")
    final.reset_index(inplace=True)

    final = final[final["Account No"].isin(df["Account No"].tolist())].copy()

    target_data = json.loads(final.T.to_json())

    sequential_data = {
        str(i + 1): value
        for i, (_, value) in enumerate(
            sorted(target_data.items(), key=lambda x: x[1]["Account No"])
        )
    }

    return sequential_data
