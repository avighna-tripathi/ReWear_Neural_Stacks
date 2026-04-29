import re
from datetime import timedelta
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from django.utils import timezone

from rewear.models import Conversation, Item, Message, Swap, UserProfile


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)


SEED_USERS = [
    {"name": "Vidushi", "email": "vidushishrinet@gmail.com", "password": "Vidushi@0604", "points": 180},
    {"name": "Avighna", "email": "avighnatripathi1102@gmail.com", "password": "Avighna@1102", "points": 210},
    {"name": "Abhay", "email": "abhay.community@rewear.local", "password": "Abhay@2026", "points": 135},
    {"name": "Bhavesh", "email": "bhavesh.community@rewear.local", "password": "Bhavesh@2026", "points": 120},
    {"name": "Mayank", "email": "mayank.community@rewear.local", "password": "Mayank@2026", "points": 145},
    {"name": "Praayashi", "email": "praayashi.community@rewear.local", "password": "Praayashi@2026", "points": 160},
    {"name": "Tammanna", "email": "tammanna.community@rewear.local", "password": "Tammanna@2026", "points": 150},
]


ITEM_SPECS = [
    {
        "owner": "Vidushi",
        "title": "Indigo Utility Denim Jacket",
        "description": "Material: Mid-weight cotton denim.\nFit: Relaxed layering fit.\nSize: M.\nCondition: Excellent.\nDetails: Button front, two chest pockets, clean stitching.",
        "category": "outerwear",
        "item_type": "Denim Jacket",
        "size": "M",
        "condition": "excellent",
        "tags": "denim,casual,layering,indigo",
        "points": 34,
        "status": "available",
        "source_page": "https://www.pexels.com/photo/close-up-photo-of-a-denim-jacket-6765179/",
    },
    {
        "owner": "Vidushi",
        "title": "Sunset Floral Midi Dress",
        "description": "Material: Soft printed poly-crepe.\nFit: Easy waist with flowy skirt.\nSize: S.\nCondition: Like new.\nDetails: Midi length, breathable lining, light occasion wear.",
        "category": "dresses",
        "item_type": "Midi Dress",
        "size": "S",
        "condition": "like-new",
        "tags": "floral,midi,summer,occasion",
        "points": 30,
        "status": "pending",
        "source_page": "https://www.pexels.com/photo/photo-of-woman-wearing-floral-dress-1573476/",
    },
    {
        "owner": "Vidushi",
        "title": "Ivory Studio Silk Blouse",
        "description": "Material: Satin-touch fabric.\nFit: Tailored semi-formal fit.\nSize: M.\nCondition: Excellent.\nDetails: Smooth finish, works for office and dinner looks.",
        "category": "tops",
        "item_type": "Silk Blouse",
        "size": "M",
        "condition": "excellent",
        "tags": "blouse,silk,formal,ivory",
        "points": 28,
        "status": "available",
        "source_page": "https://www.pexels.com/photo/portrait-of-woman-wearing-silk-blouse-19652513/",
    },
    {
        "owner": "Avighna",
        "title": "Minimal White Court Sneakers",
        "description": "Material: Synthetic upper with rubber sole.\nFit: Everyday comfort fit.\nSize: UK 9.\nCondition: Good.\nDetails: Clean silhouette, easy to pair with denim or joggers.",
        "category": "shoes",
        "item_type": "Sneakers",
        "size": "UK 9",
        "condition": "good",
        "tags": "sneakers,white,streetwear,daily",
        "points": 24,
        "status": "available",
        "source_page": "https://www.pexels.com/photo/photo-of-white-sneakers-6050912/",
    },
    {
        "owner": "Avighna",
        "title": "Brown Weekend Leather Boots",
        "description": "Material: Leather upper.\nFit: Firm ankle support.\nSize: UK 9.\nCondition: Good.\nDetails: Textured finish, durable sole, travel-friendly pair.",
        "category": "shoes",
        "item_type": "Leather Boots",
        "size": "UK 9",
        "condition": "good",
        "tags": "boots,leather,brown,weekend",
        "points": 32,
        "status": "swapped",
        "source_page": "https://www.pexels.com/photo/a-person-wearing-leather-boots-13347812/",
    },
    {
        "owner": "Avighna",
        "title": "Layered Street Denim Jacket",
        "description": "Material: Durable blue denim.\nFit: Easy relaxed fit.\nSize: L.\nCondition: Excellent.\nDetails: Layering-friendly cut with standout casual styling.",
        "category": "outerwear",
        "item_type": "Jacket",
        "size": "L",
        "condition": "excellent",
        "tags": "denim,jacket,streetwear,blue",
        "points": 36,
        "status": "pending",
        "source_page": "https://www.pexels.com/photo/a-man-wearing-a-denim-jacket-6772737/",
    },
    {
        "owner": "Abhay",
        "title": "Cozy Oatmeal Wool Sweater",
        "description": "Material: Wool blend knit.\nFit: Regular winter fit.\nSize: L.\nCondition: Excellent.\nDetails: Soft hand feel, ideal for office layering and cool evenings.",
        "category": "tops",
        "item_type": "Sweater",
        "size": "L",
        "condition": "excellent",
        "tags": "sweater,wool,winter,neutral",
        "points": 26,
        "status": "available",
        "source_page": "https://www.pexels.com/photo/wool-sweater-and-jeans-15667095/",
    },
    {
        "owner": "Abhay",
        "title": "Relaxed Blue Denim Jeans",
        "description": "Material: Soft-wash denim.\nFit: Relaxed straight cut.\nSize: 32.\nCondition: Good.\nDetails: Mid-rise, easy everyday pair, no tear or fading spots.",
        "category": "bottoms",
        "item_type": "Jeans",
        "size": "32",
        "condition": "good",
        "tags": "jeans,denim,basics,straight-fit",
        "points": 22,
        "status": "available",
        "source_page": "https://www.pexels.com/photo/a-woman-wearing-denim-jeans-13137728/",
    },
    {
        "owner": "Abhay",
        "title": "Clean White Commuter Sneakers",
        "description": "Material: Faux leather upper.\nFit: Lightweight low-top.\nSize: UK 8.\nCondition: Like new.\nDetails: Sleek casual pair for city errands and campus wear.",
        "category": "shoes",
        "item_type": "Sneakers",
        "size": "UK 8",
        "condition": "like-new",
        "tags": "sneakers,white,city,minimal",
        "points": 23,
        "status": "pending",
        "source_page": "https://www.pexels.com/photo/photo-of-white-sneakers-4252969/",
    },
    {
        "owner": "Bhavesh",
        "title": "Field Blue Denim Jacket",
        "description": "Material: Structured denim shell.\nFit: Slightly boxy fit.\nSize: M.\nCondition: Excellent.\nDetails: Strong collar shape, versatile for smart-casual looks.",
        "category": "outerwear",
        "item_type": "Jacket",
        "size": "M",
        "condition": "excellent",
        "tags": "jacket,denim,blue,casual",
        "points": 33,
        "status": "available",
        "source_page": "https://www.pexels.com/photo/model-in-denim-jacket-16286312/",
    },
    {
        "owner": "Bhavesh",
        "title": "Street White Lace Sneakers",
        "description": "Material: Faux leather upper.\nFit: Low-top comfort fit.\nSize: UK 8.\nCondition: Like new.\nDetails: Crisp white finish, light sole, ideal for daily campus wear.",
        "category": "shoes",
        "item_type": "Lace Sneakers",
        "size": "UK 8",
        "condition": "like-new",
        "tags": "white,sneakers,lace-up,minimal",
        "points": 25,
        "status": "swapped",
        "source_page": "https://www.pexels.com/photo/white-shoes-on-white-background-7193626/",
    },
    {
        "owner": "Bhavesh",
        "title": "Structured Urban Handbag",
        "description": "Material: Black leather exterior.\nFit: Medium daily carry.\nSize: One Size.\nCondition: Excellent.\nDetails: Zip closure, polished metal accents, easy everyday organization.",
        "category": "accessories",
        "item_type": "Handbag",
        "size": "One Size",
        "condition": "excellent",
        "tags": "bag,black,structured,everyday",
        "points": 37,
        "status": "available",
        "source_page": "https://www.pexels.com/photo/a-black-leather-handbag-6167276/",
    },
    {
        "owner": "Mayank",
        "title": "Winter Knit Wool Pullover",
        "description": "Material: Chunky wool blend.\nFit: Comfortable relaxed fit.\nSize: XL.\nCondition: Excellent.\nDetails: Warm texture, pairs well with denims and chinos.",
        "category": "tops",
        "item_type": "Pullover",
        "size": "XL",
        "condition": "excellent",
        "tags": "pullover,wool,chunky,winter",
        "points": 28,
        "status": "available",
        "source_page": "https://www.pexels.com/photo/choice-of-wool-sweaters-15000716/",
    },
    {
        "owner": "Mayank",
        "title": "Craft Brown Leather Boots",
        "description": "Material: Leather outer with stitched sole.\nFit: Supportive ankle fit.\nSize: UK 10.\nCondition: Good.\nDetails: Rugged styling, ideal for denim and winter layers.",
        "category": "shoes",
        "item_type": "Boots",
        "size": "UK 10",
        "condition": "good",
        "tags": "boots,brown,leather,rugged",
        "points": 35,
        "status": "available",
        "source_page": "https://www.pexels.com/photo/photograph-of-leather-boots-13106333/",
    },
    {
        "owner": "Mayank",
        "title": "Smart Indigo Denim Jacket",
        "description": "Material: Mid-weight denim.\nFit: Straight modern fit.\nSize: L.\nCondition: Excellent.\nDetails: Sharp collar, easy layering, subtle urban look.",
        "category": "outerwear",
        "item_type": "Jacket",
        "size": "L",
        "condition": "excellent",
        "tags": "denim,jacket,smart,indigo",
        "points": 35,
        "status": "pending",
        "source_page": "https://www.pexels.com/photo/man-wearing-denim-jacket-2744951/",
    },
    {
        "owner": "Praayashi",
        "title": "Ivory Satin-Look Silk Blouse",
        "description": "Material: Smooth satin-finish fabric.\nFit: Soft drape, semi-formal cut.\nSize: M.\nCondition: Like new.\nDetails: Easy office-to-evening piece with clean neckline.",
        "category": "tops",
        "item_type": "Blouse",
        "size": "M",
        "condition": "like-new",
        "tags": "blouse,ivory,formal,satin",
        "points": 29,
        "status": "available",
        "source_page": "https://www.pexels.com/photo/portrait-of-woman-wearing-silk-blouse-19652510/",
    },
    {
        "owner": "Praayashi",
        "title": "Meadow Floral Day Dress",
        "description": "Material: Lightweight woven blend.\nFit: Waist-skimming and airy.\nSize: S.\nCondition: Excellent.\nDetails: Easy brunch or daytime event dress, vibrant print.",
        "category": "dresses",
        "item_type": "Day Dress",
        "size": "S",
        "condition": "excellent",
        "tags": "dress,floral,daywear,print",
        "points": 31,
        "status": "swapped",
        "source_page": "https://www.pexels.com/photo/a-woman-wearing-floral-dress-7679595/",
    },
    {
        "owner": "Praayashi",
        "title": "Evening Gloss Silk Top",
        "description": "Material: Lustrous silky weave.\nFit: Dressy regular fit.\nSize: M.\nCondition: Excellent.\nDetails: Rich sheen and elegant finish for evening styling.",
        "category": "tops",
        "item_type": "Silk Top",
        "size": "M",
        "condition": "excellent",
        "tags": "silk,evening,glossy,top",
        "points": 30,
        "status": "available",
        "source_page": "https://www.pexels.com/photo/elegant-portrait-of-woman-in-silk-blouse-34267942/",
    },
    {
        "owner": "Tammanna",
        "title": "Structured Black Leather Handbag",
        "description": "Material: Leather exterior.\nFit: Medium structured carry.\nSize: One Size.\nCondition: Excellent.\nDetails: Sleek shape, clean hardware, practical daily-carry size.",
        "category": "accessories",
        "item_type": "Handbag",
        "size": "One Size",
        "condition": "excellent",
        "tags": "handbag,black,leather,structured",
        "points": 38,
        "status": "available",
        "source_page": "https://www.pexels.com/photo/handbag-5670/",
    },
    {
        "owner": "Tammanna",
        "title": "Soft Blue Everyday Jeans",
        "description": "Material: Washed denim.\nFit: Relaxed ankle-length fit.\nSize: 28.\nCondition: Good.\nDetails: Comfortable all-day pair with clean hem and soft fade.",
        "category": "bottoms",
        "item_type": "Jeans",
        "size": "28",
        "condition": "good",
        "tags": "jeans,blue,everyday,relaxed",
        "points": 21,
        "status": "available",
        "source_page": "https://www.pexels.com/photo/person-wearing-denim-jeans-14517734/",
    },
    {
        "owner": "Tammanna",
        "title": "Garden Floral Weekend Dress",
        "description": "Material: Soft printed day fabric.\nFit: Relaxed flowy fit.\nSize: M.\nCondition: Like new.\nDetails: Easy summer dress with vibrant floral pattern and movement.",
        "category": "dresses",
        "item_type": "Weekend Dress",
        "size": "M",
        "condition": "like-new",
        "tags": "dress,floral,weekend,summer",
        "points": 29,
        "status": "pending",
        "source_page": "https://www.pexels.com/photo/a-woman-wearing-floral-dress-7924035/",
    },
]


SWAP_SPECS = [
    {
        "item_title": "Brown Weekend Leather Boots",
        "initiator": "Vidushi",
        "recipient": "Avighna",
        "status": "completed",
        "points_delta": 32,
        "note": "Completed as a points redemption after a sizing chat.",
        "days_ago": 18,
    },
    {
        "item_title": "Street White Lace Sneakers",
        "initiator": "Abhay",
        "recipient": "Bhavesh",
        "status": "completed",
        "points_delta": 25,
        "note": "Campus handoff completed successfully.",
        "days_ago": 12,
    },
    {
        "item_title": "Meadow Floral Day Dress",
        "initiator": "Tammanna",
        "recipient": "Praayashi",
        "status": "completed",
        "points_delta": 31,
        "note": "Weekend swap completed through direct exchange.",
        "days_ago": 8,
    },
    {
        "item_title": "Sunset Floral Midi Dress",
        "initiator": "Mayank",
        "recipient": "Vidushi",
        "status": "pending",
        "points_delta": 30,
        "note": "Requested for an upcoming family event.",
        "days_ago": 3,
    },
    {
        "item_title": "Layered Street Denim Jacket",
        "initiator": "Praayashi",
        "recipient": "Avighna",
        "status": "pending",
        "points_delta": 36,
        "note": "Waiting on fit confirmation.",
        "days_ago": 2,
    },
    {
        "item_title": "Clean White Commuter Sneakers",
        "initiator": "Tammanna",
        "recipient": "Abhay",
        "status": "pending",
        "points_delta": 23,
        "note": "Reserved while pickup timing is finalized.",
        "days_ago": 1,
    },
]


class Command(BaseCommand):
    help = "Seed sample community users, product listings, and swap history."

    def handle(self, *args, **options):
        users_by_name = {}
        for user_data in SEED_USERS:
            user, _ = User.objects.get_or_create(
                username=user_data["email"],
                defaults={"email": user_data["email"], "first_name": user_data["name"], "last_name": ""},
            )
            user.email = user_data["email"]
            user.first_name = user_data["name"]
            user.last_name = ""
            user.set_password(user_data["password"])
            user.save()

            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.points = user_data["points"]
            profile.save()
            users_by_name[user_data["name"]] = user

        items_by_title = {}
        for item_data in ITEM_SPECS:
            owner = users_by_name[item_data["owner"]]
            item, _ = Item.objects.update_or_create(
                owner=owner,
                title=item_data["title"],
                defaults={
                    "description": item_data["description"],
                    "category": item_data["category"],
                    "item_type": item_data["item_type"],
                    "size": item_data["size"],
                    "condition": item_data["condition"],
                    "tags": item_data["tags"],
                    "points": item_data["points"],
                    "status": item_data["status"],
                    "current_holder": owner,
                },
            )
            items_by_title[item.title] = item

            if not item.image:
                image_content, image_extension = self.fetch_image_from_page(item_data["source_page"])
                image_name = f"{slugify(owner.first_name)}-{slugify(item.title)}{image_extension}"
                item.image.save(image_name, image_content, save=True)

        for swap_data in SWAP_SPECS:
            item = items_by_title[swap_data["item_title"]]
            initiator = users_by_name[swap_data["initiator"]]
            recipient = users_by_name[swap_data["recipient"]]
            swap, _ = Swap.objects.update_or_create(
                item=item,
                initiator=initiator,
                recipient=recipient,
                defaults={
                    "status": swap_data["status"],
                    "points_delta": swap_data["points_delta"],
                    "note": swap_data["note"],
                    "completed_at": timezone.now() - timedelta(days=swap_data["days_ago"])
                    if swap_data["status"] == "completed"
                    else None,
                },
            )
            created_at = timezone.now() - timedelta(days=swap_data["days_ago"])
            Swap.objects.filter(pk=swap.pk).update(created_at=created_at)
            participant_one, participant_two = (initiator, recipient) if initiator.id <= recipient.id else (recipient, initiator)
            conversation, _ = Conversation.objects.get_or_create(
                item=item,
                participant_one=participant_one,
                participant_two=participant_two,
                defaults={"swap": swap},
            )
            if conversation.swap_id != swap.id:
                conversation.swap = swap
                conversation.save(update_fields=["swap", "updated_at"])
            if not conversation.messages.exists():
                Message.objects.create(
                    conversation=conversation,
                    sender=initiator,
                    body=swap_data["note"],
                )

            if swap.status == "completed":
                item.status = "swapped"
                item.current_holder = initiator
                item.save(update_fields=["status", "current_holder"])
            elif swap.status == "pending":
                item.status = "pending"
                item.current_holder = recipient
                item.save(update_fields=["status", "current_holder"])

        self.stdout.write(self.style.SUCCESS("Sample community users, products, and swaps created."))

    def fetch_image_from_page(self, page_url):
        html = self.fetch_bytes(page_url).decode("utf-8", errors="ignore")
        match = re.search(
            r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']',
            html,
            re.IGNORECASE,
        )
        if not match:
            match = re.search(
                r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']',
                html,
                re.IGNORECASE,
            )
        if not match:
            raise ValueError(f"Could not find og:image for {page_url}")

        image_url = match.group(1)
        image_bytes = self.fetch_bytes(image_url)
        parsed = urlparse(image_url)
        extension = Path(parsed.path).suffix.lower() or ".jpg"
        if extension not in {".jpg", ".jpeg", ".png", ".webp"}:
            extension = ".jpg"
        return ContentFile(image_bytes), extension

    def fetch_bytes(self, url):
        request = Request(url, headers={"User-Agent": USER_AGENT})
        with urlopen(request, timeout=30) as response:
            return response.read()
