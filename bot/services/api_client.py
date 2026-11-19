from aiohttp import ClientSession
from bot.schemas.get_schedule import GetScheduleByGroup, GetScheduleByName
from bs4 import BeautifulSoup

class ApiClient:
    def __init__(self, session: ClientSession, schedule_url: str) -> None:
        self.session: ClientSession = session
        self.schedule_url: str = schedule_url

    async def get_schedule_by_group(self, request: GetScheduleByGroup) -> dict:
        async with self.session.get(f"{self.schedule_url}/{request.week}/{request.group}") as response:
            page = await response.text()
            return self.parse_response(page)


    async def get_schedule_by_name(self, request: GetScheduleByName) -> dict:
        async with self.session.get(f"{self.schedule_url}/{request.week}?tutor_name={request.name}") as response:
            page = await response.text()
            return self.parse_response(page)


    @staticmethod
    def parse_response(page) -> dict:
        soup = BeautifulSoup(page, 'html.parser')

        group_name = "Неизвестно"
        week_number = "Неизвестно"

        group_div = soup.find('div', class_='section__title')
        if group_div:
            h3 = group_div.find('h3')
            if h3:
                text = h3.get_text(strip=True)
                if 'ГРУППА' in text:
                    group_name = text.split('ГРУППА')[0].strip()
                if 'учебная неделя' in text:
                    week_number = text.split('Выбрано:')[-1].strip() if 'Выбрано:' in text else text.strip()

        table = soup.find('table')
        if not table:
            return {"error": "Таблица не найдена", "schedule": [], "group": group_name, "week": week_number}

        schedule = []
        current_day = None

        for row in table.find_all('tr'):
            day_cell = row.find('td', class_='vertical-text')
            if day_cell:
                current_day = day_cell.get_text(strip=True)
                continue
            cells = row.find_all('td')
            if current_day and len(cells) >= 5:
                time = cells[0].get_text(strip=True)
                subject = cells[1].get_text(strip=True)
                teacher = cells[2].get_text(strip=True)
                room = cells[4].get_text(strip=True) if len(cells) > 4 else ""
                if time and subject and not any(skip in subject.lower()
                                                for skip in ['кураторский', 'информационный']):
                    schedule.append({
                        "day": current_day,
                        "time": time,
                        "subject": subject,
                        "teacher": teacher,
                        "room": room
                    })

        return {
            "group": group_name,
            "week": week_number,
            "schedule": schedule
        }
