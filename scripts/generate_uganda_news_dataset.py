import argparse
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


REAL_TITLES = [
    "Government launches new digital identity registration drive in Kampala",
    "Uganda secures funding for rural electricity expansion",
    "Ministry of Health reports improved vaccination uptake in western Uganda",
    "Transport operators set new commuter fares after fuel price review",
    "Ugandan farmers receive support for maize and rice production",
    "National school exam results show improved performance in central region",
    "Local businesses in Entebbe report growth in tourism bookings",
    "Water authority expands pipe network in Jinja and Iganga",
    "Parliament debates budget priorities for agriculture and roads",
    "Kampala city authorities open new market stall zones for traders",
    "University students begin innovation hackathon in Makerere",
    "Police launch community road safety campaign along major highways",
    "Uganda signs new trade cooperation deal with regional partners",
    "Bank of Uganda releases update on inflation and lending rates",
    "Farmers in Hoima receive subsidized seedlings for climate resilience",
    "Regional tourism board highlights increase in visitors to national parks",
    "New public transport routes improve access in Wakiso district",
    "District health teams roll out malaria prevention outreach in schools",
    "Electricity regulator approves new grid maintenance program",
    "Smallholder cooperatives secure agricultural financing from local lenders",
    "University researchers begin pilot project on solar-powered irrigation",
    "Tax authority calls for compliance as filing season opens in Uganda",
    "Construction of new hospital wing reaches completion in Mbale",
    "District council approves waste management plan for urban centres",
    "Youth employment scheme expands training opportunities in northern Uganda",
    "National telecom provider upgrades internet services in eastern Uganda",
    "Fisheries officers inspect landing sites after seasonal monitoring review",
    "Rural clinics receive medical equipment under government supply program",
    "Uganda hosts regional conference on cross-border trade and logistics",
    "Municipal council unveils plan to rehabilitate drainage channels in flood-prone areas",
    "Tour operators report steady growth in birding and eco-tourism bookings",
]

FAKE_TITLES = [
    "Breaking: President secretly plans to relocate the capital to a floating island",
    "Shocking video shows government officials eating snakes to avoid taxes",
    "Scientists confirm a mysterious underground lake under Kampala is producing electricity",
    "Exclusive: Foreign investors plan to buy all Ugandan land for a giant AI city",
    "Doctors reveal a miracle cure for malaria discovered in a roadside market",
    "Government announces all boda boda riders will be replaced by drones next month",
    "Viral claim says a military helicopter was seen landing at Lake Victoria with gold",
    "International experts warn that all Ugandan schools will switch to underwater classrooms",
    "Local radio report says a hidden tunnel connects Uganda to a foreign embassy",
    "Residents panic as the moon appears to be turning red over central Uganda",
    "Secret memo says all civil servants must drink herbal medicine from a single supplier",
    "Breaking: Army confirms alien objects were recovered near Mbarara",
    "Celebrity pastor claims he can stop floods with a single prayer ceremony",
    "Authorities ban all tomatoes after a mysterious overnight contamination rumour",
    "Unverified report says a famous singer is buying every school in western Uganda",
    "Whistleblower reveals the true reason behind the new road project in Kampala",
    "Rumour spreads that every district will receive free gold bars for citizens",
    "Hidden document claims Uganda is building a giant underground train beneath the capital",
    "Shock: Entire village in Busoga reportedly lives on a buried treasure map",
    "Residents say an abandoned cargo plane landed in northern Uganda carrying medicine",
    "Officials allegedly plan to replace all school uniforms with military gear",
    "Breaking: New law will require citizens to plant only one crop nationwide",
    "Villagers claim a giant stone from the sky landed near Fort Portal",
    "Internet rumour says the president has ordered all roads to be painted green",
    "Scientists say a secret mushroom can cure diabetes and HIV in a single dose",
    "Town leads launch of anti-ghost initiative after citizens report midnight phantom buses",
]

REAL_CONTENT_PARTS = [
    "Officials said the programme would improve service delivery and expand access to underserved communities.",
    "Local leaders welcomed the update and called for regular monitoring to ensure implementation remains on schedule.",
    "Residents said the developments would reduce travel time and support commerce in the area.",
    "The announcement follows consultations with district teams, transport operators and community representatives.",
    "Authorities said the plan would strengthen public services and improve accountability in the delivery of basic needs.",
    "Analysts noted that the move could improve household income and support local manufacturing and trade.",
    "Officials urged communities to cooperate with monitoring teams and continue submitting feedback on service quality.",
    "The project is expected to benefit schools, clinics and major commercial centres in the surrounding areas.",
    "District officials said the investment would help cut costs, improve access and create more job opportunities.",
    "The statement was released after a review by technical teams, local leaders and stakeholders from the private sector.",
]

FAKE_CONTENT_PARTS = [
    "The story spread rapidly on social media, with many people sharing the claim without verification.",
    "Witnesses described the event as unusual and said it could not be explained by normal local activity.",
    "Supporters of the claim insisted the information was credible, even though no official source had confirmed it.",
    "Experts who reviewed the clip said the footage appeared unusual but lacked independent verification.",
    "Several online users claimed the allegation was proof of a larger hidden plan involving public institutions.",
    "The message was repeated widely before any formal confirmation by authorities or accredited media houses.",
    "Activists said the story offered evidence of a secret operation that had not been acknowledged publicly.",
    "The claim generated mixed reactions, with some people calling it a major revelation and others dismissing it as a hoax.",
    "Even though no proof was provided, the rumour gained traction through online groups and forwarded messages.",
    "Followers of the claim said the evidence was clear, although no independent document or statement was published.",
]

SOURCES = [
    "Daily Monitor",
    "New Vision",
    "The Observer",
    "Monitor",
    "Bukedde",
    "NTV Uganda",
    "Urban TV",
    "UBC",
    "Kampala Sun",
    "Uganda Today",
    "The Independent",
    "Nile Post",
    "ChimpReports",
    "Uganda Radio Network",
    "East African Business Week",
]

CATEGORIES = [
    "politics",
    "business",
    "health",
    "education",
    "transport",
    "agriculture",
    "technology",
    "tourism",
    "environment",
    "sports",
]


def random_date(start_year=2022, end_year=2025):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta_days = (end - start).days
    random_day = start + timedelta(days=random.randint(0, delta_days))
    return random_day.strftime("%Y-%m-%d")


def build_real_article(index: int) -> dict:
    title = REAL_TITLES[index % len(REAL_TITLES)]
    body = " ".join([
        title,
        random.choice(REAL_CONTENT_PARTS),
        "The update was shared during a public briefing attended by district officials and community leaders.",
        "Stakeholders said the measures would improve planning, transparency and service delivery across the affected areas.",
        "The development is part of a wider effort to support economic activity and improve public accountability in Uganda.",
    ])
    source = random.choice(SOURCES)
    category = random.choice(CATEGORIES)
    return {
        "id": index + 1,
        "title": title,
        "content": body,
        "source": source,
        "date": random_date(),
        "category": category,
        "label": "real",
        "country": "Uganda",
        "language": "en",
        "url": f"https://example.org/ug/real/{index + 1}",
        "article_type": "real_news",
    }


def build_fake_article(index: int) -> dict:
    title = FAKE_TITLES[index % len(FAKE_TITLES)]
    body = " ".join([
        title,
        random.choice(FAKE_CONTENT_PARTS),
        "The claim was shared widely across messaging groups and online communities before any official confirmation was issued.",
        "Many readers questioned the source, but the message continued circulating because it was described as a major revelation.",
        "No verified public record was found to support the story, but the rumour remained active across several online networks.",
    ])
    source = random.choice(["WhatsApp rumour", "Facebook viral post", "Unverified social media claim", "Blog post", "Viral message chain"])
    category = random.choice(["politics", "health", "technology", "society", "economy", "environment"])
    return {
        "id": index + 1,
        "title": title,
        "content": body,
        "source": source,
        "date": random_date(),
        "category": category,
        "label": "fake",
        "country": "Uganda",
        "language": "en",
        "url": f"https://example.org/ug/fake/{index + 1}",
        "article_type": "fake_news",
    }


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic Uganda real and fake news CSV files.")
    parser.add_argument("--real-count", type=int, default=20000)
    parser.add_argument("--fake-count", type=int, default=20000)
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parents[1]
    data_dir = base_dir / "data"
    fieldnames = [
        "id",
        "title",
        "content",
        "source",
        "date",
        "category",
        "label",
        "country",
        "language",
        "url",
        "article_type",
    ]

    real_rows = [build_real_article(i) for i in range(args.real_count)]
    fake_rows = [build_fake_article(i) for i in range(args.fake_count)]

    write_csv(data_dir / "uganda_real_news.csv", real_rows, fieldnames)
    write_csv(data_dir / "uganda_fake_news.csv", fake_rows, fieldnames)

    print(f"Generated {len(real_rows)} real-news rows at {data_dir / 'uganda_real_news.csv'}")
    print(f"Generated {len(fake_rows)} fake-news rows at {data_dir / 'uganda_fake_news.csv'}")


if __name__ == "__main__":
    main()

