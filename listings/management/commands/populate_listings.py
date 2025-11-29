import os
import urllib.request
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from listings.models import Listing, User
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Populate database with 20 sample listings'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating listings...')

        # List of 20 Unsplash Image IDs for houses/interiors
        image_ids = [
            '1570129477492-45c003edd2be', # Modern house
            '1564013799919-ab600027ffc6', # Luxury home
            '1580587771525-78b9dba3b91d', # Cottage
            '1518780664697-55e3ad937233', # House with garden
            '1600596542815-2495db9dc2c3', # Modern interior
            '1512917774080-9991f1c4c750', # Luxury apartment
            '1572120360610-d971b9d7767c', # Cozy cabin
            '1568605114967-8130f3a36994', # Suburban house
            '1598228723793-52759bba239c', # Vacation rental
            '1583608205776-bfd35f0d9f83', # Modern loft
            '1576941089067-2de3c901e126', # Family home
            '1599809275372-b40c3691b9cc', # Beach house
            '1600585154340-be6161a56a0c', # Pool house
            '1600607687939-ce8a6c25118c', # Modern kitchen
            '1600566753190-17f0baa2a6c3', # Living room
            '1600585154526-990dced4db0d', # Bedroom
            '1554995207-c18c203602cb',    # Apartment interior
            '1502672260266-1c1ef2d93688', # Loft
            '1502005229766-528352252143', # Classic home
            '1560448204-e02f11c3d0e2',    # Real estate
        ]

        titles = [
            "Modern Beach Villa", "Cozy Mountain Cabin", "Luxury City Apartment", "Secluded Lake House",
            "Rustic Country Cottage", "Downtown Loft", "Sunny Garden Home", "Historic Townhouse",
            "Spacious Family Retreat", "Minimalist Studio", "Ocean View Penthouse", "Forest Hideaway",
            "Desert Oasis", "Charming Bungalow", "Elegant Manor", "Ski Chalet",
            "Riverside Lodge", "Urban Sanctuary", "Vintage Farmhouse", "Contemporary Glass House"
        ]

        cities = [
            "Malibu", "Aspen", "New York", "Lake Tahoe", "Nashville", "Chicago", "Austin", "Boston",
            "Orlando", "San Francisco", "Miami", "Portland", "Phoenix", "Savannah", "London", "Denver",
            "Seattle", "Los Angeles", "Vermont", "Vancouver"
        ]
        
        countries = ["USA", "USA", "USA", "USA", "USA", "USA", "USA", "USA", "USA", "USA", "USA", "USA", "USA", "USA", "UK", "USA", "USA", "USA", "USA", "Canada"]

        # Coordinates for each city (approximate)
        coordinates = [
            (34.0259, -118.7798), # Malibu
            (39.1911, -106.8175), # Aspen
            (40.7128, -74.0060),  # New York
            (39.0968, -120.0324), # Lake Tahoe
            (36.1627, -86.7816),  # Nashville
            (41.8781, -87.6298),  # Chicago
            (30.2672, -97.7431),  # Austin
            (42.3601, -71.0589),  # Boston
            (28.5383, -81.3792),  # Orlando
            (37.7749, -122.4194), # San Francisco
            (25.7617, -80.1918),  # Miami
            (45.5152, -122.6784), # Portland
            (33.4484, -112.0740), # Phoenix
            (32.0809, -81.0912),  # Savannah
            (51.5074, -0.1278),   # London
            (39.7392, -104.9903), # Denver
            (47.6062, -122.3321), # Seattle
            (34.0522, -118.2437), # Los Angeles
            (44.5588, -72.5778),  # Vermont
            (49.2827, -123.1207)  # Vancouver
        ]

        categories = ['beach', 'cabins', 'lakefront', 'views', 'castles']

        for i in range(20):
            username = f'host_{i+1}'
            email = f'host_{i+1}@example.com'
            password = 'password123'

            # Create User
            user, created = User.objects.get_or_create(username=username, email=email)
            if created:
                user.set_password(password)
                user.is_host = True
                user.save()
                self.stdout.write(f'Created user: {username}')
            else:
                self.stdout.write(f'User {username} already exists')

            # Listing Details
            title = titles[i]
            city = cities[i]
            country = countries[i]
            price = random.randint(100, 500)
            category = random.choice(categories)
            image_id = image_ids[i]
            image_url = f"https://images.unsplash.com/photo-{image_id}?auto=format&fit=crop&w=800&q=80"
        # Detailed descriptions for each listing
        descriptions = [
            "Escape to this stunning Modern Beach Villa in Malibu, where luxury meets the ocean. This architectural masterpiece offers panoramic views of the Pacific Ocean from every room. The open-concept living area features floor-to-ceiling glass walls that blur the line between indoors and outdoors. Relax on the expansive deck, complete with a private infinity pool and comfortable lounge seating. The gourmet kitchen is equipped with top-of-the-line appliances, perfect for preparing seaside meals. Each bedroom is a sanctuary of peace, featuring plush bedding and en-suite bathrooms with spa-like amenities. Direct beach access allows you to enjoy morning walks on the sand or sunset swims in the ocean. Located just minutes from world-class dining and shopping, yet secluded enough to offer complete privacy. Experience the ultimate California lifestyle in this exclusive retreat. Whether you're looking for a romantic getaway or a family vacation, this villa has it all. Enjoy the sound of the waves crashing against the shore as you drift off to sleep. The villa also includes a home theater, a wine cellar, and a fully equipped gym. Private parking is available for multiple vehicles. Our dedicated concierge team is on hand to ensure your stay is flawless. Book your stay today and create unforgettable memories in this slice of paradise. Wake up to the smell of salt air and the warmth of the sun. Indulge in a private chef experience or a massage on the deck. This is more than just a vacation rental; it's a lifestyle experience. Don't miss the chance to stay in one of Malibu's most prestigious properties. Your dream beach vacation awaits.",

            "Nestled in the heart of the Rockies, this Cozy Mountain Cabin in Aspen is your perfect alpine escape. Surrounded by towering pines and majestic peaks, this cabin offers a true connection to nature. The interior features a grand stone fireplace, soaring vaulted ceilings, and rustic timber accents. After a day on the slopes, warm up by the fire with a cup of hot cocoa. The fully equipped kitchen has everything you need to cook hearty mountain meals. The master suite boasts a king-sized bed and a private balcony with breathtaking views. Step outside to the spacious wrap-around porch and soak in the private hot tub under the stars. Located just a short drive from downtown Aspen, you have easy access to skiing, hiking, and dining. This cabin is the ideal base for outdoor adventures in every season. In the summer, explore the nearby trails and wildflowers. In the winter, enjoy world-class skiing and snowboarding just minutes away. The cabin is equipped with high-speed Wi-Fi and a smart TV for your entertainment. A washer and dryer are provided for your convenience. Experience the charm of mountain living with all the modern comforts. Perfect for couples, families, or small groups of friends. Listen to the wind in the trees and the silence of the snow. Create lasting memories in this enchanting mountain hideaway. Wildlife sightings are common, so keep your camera ready. Escape the hustle and bustle and find your peace in the mountains. Welcome to your home away from home in Aspen.",

            "Experience the height of luxury in this City Apartment located in the heart of New York. This sophisticated residence offers stunning skyline views through floor-to-ceiling windows. The modern design features sleek lines, premium finishes, and curated art pieces. The spacious living room is perfect for entertaining or relaxing after a day in the city. A state-of-the-art kitchen awaits the culinary enthusiast, complete with marble countertops. The bedroom is a quiet oasis above the bustling streets, ensuring a restful night's sleep. Located in a prestigious building with a 24-hour doorman and fitness center. You are steps away from Central Park, Broadway theaters, and Fifth Avenue shopping. Immerse yourself in the vibrant culture and energy of the Big Apple. The apartment is equipped with smart home technology for lighting and climate control. High-speed internet and a dedicated workspace make it ideal for business travelers. Enjoy a morning coffee on the private balcony overlooking the city. The bathroom features a rain shower and deep soaking tub for ultimate relaxation. This is the perfect launchpad for exploring everything New York City has to offer. From world-class museums to hidden jazz clubs, it's all at your doorstep. Live like a local in one of the city's most desirable neighborhoods. Concierge services are available to assist with reservations and tickets. Experience the luxury and convenience of city living at its finest. Your urban sanctuary awaits in the city that never sleeps. Book now for an unforgettable New York experience.",

            "Discover tranquility at this Secluded Lake House on the shores of Lake Tahoe. Hidden among the trees, this property offers unmatched privacy and direct lake access. The house features a classic lodge design with a modern twist, warm and inviting. Large windows frame the turquoise waters of the lake and the surrounding mountains. The living room centers around a massive stone fireplace, perfect for cozy evenings. A gourmet kitchen and large dining area make it easy to host family and friends. Step out onto the private dock for swimming, boating, or simply soaking up the sun. The expansive deck is equipped with a BBQ grill and outdoor dining furniture. Enjoy hiking trails right from your doorstep or take a short drive to ski resorts. The master bedroom offers waking up to the sunrise over the lake. Each room is tastefully decorated to reflect the natural beauty of the area. A game room with a pool table provides entertainment for all ages. Relax in the outdoor hot tub while watching the sunset over the water. This is the ultimate year-round destination for nature lovers. Whether it's summer water sports or winter skiing, Tahoe has it all. The property includes a garage and ample parking for guests. Experience the crystal-clear waters and fresh mountain air. Disconnect from the world and reconnect with loved ones in this serene setting. A true gem on the lake, waiting for your arrival. Make this lake house your tradition for years to come.",

            "Step back in time with modern comforts in this Rustic Country Cottage in Nashville. Located in a peaceful setting just outside the city, it offers the best of both worlds. The cottage features reclaimed wood floors, exposed beams, and vintage decor. The cozy living room invites you to curl up with a good book or enjoy a movie. A fully equipped country kitchen allows you to whip up delicious southern meals. Enjoy your morning coffee on the swing of the charming front porch. The backyard is a private oasis with a fire pit, perfect for roasting marshmallows. Listen to the sounds of nature and enjoy the slow pace of country living. You are just a short Uber ride away from the honky-tonks of Broadway. Explore the local music scene, history, and incredible food of Nashville. The bedroom features a comfortable queen bed with high-quality linens. The bathroom includes a clawfoot tub for a relaxing soak. This cottage is a songwriter's dream, inspiring and serene. Perfect for a romantic getaway or a solo retreat. Experience the famous southern hospitality in this unique home. The property is pet-friendly, so bring your furry friend along. Wi-Fi and streaming services are included for your convenience. Discover the hidden gems of Nashville from this lovely base. A truly unique stay that captures the spirit of Music City. Come and stay a while in this rustic charm.",

            "Immerse yourself in the architectural marvel of this Downtown Loft in Chicago. Located in a historic building, this loft features high ceilings and exposed brick walls. Huge industrial windows flood the space with natural light and offer city views. The open-plan layout creates a spacious and airy atmosphere. Furnished with a mix of modern and vintage pieces for an eclectic vibe. The kitchen is a chef's delight with a large island and professional-grade appliances. The sleeping area is separated by stylish dividers for privacy. Located in the Loop, you are walking distance to Millennium Park and the Art Institute. Experience the vibrant dining and nightlife scene of Chicago right outside your door. The building offers a rooftop deck with panoramic views of the skyline. Perfect for business travelers or couples looking for a chic city stay. High-speed Wi-Fi and a dedicated workspace are provided. The bathroom features a modern walk-in shower and premium toiletries. Enjoy the convenience of in-unit laundry. Explore the riverwalk or take an architecture boat tour nearby. This loft embodies the cool, urban spirit of Chicago. Live in style and comfort in the heart of the Windy City. Secure entry and elevator access ensure your safety and ease. Book your stay in this iconic Chicago loft today. Your urban adventure starts here.",

            "Soak up the sun in this Sunny Garden Home in the vibrant city of Austin. This colorful and quirky home reflects the unique spirit of Austin. The highlight is the lush, private garden with native plants and outdoor seating. Inside, you'll find a bright and cheerful living space with eclectic art. The kitchen is fully stocked and features a breakfast nook overlooking the garden. Two comfortable bedrooms offer a restful retreat after exploring the city. Located in a trendy neighborhood, walkable to food trucks and coffee shops. Enjoy a BBQ in the backyard or relax in the hammock under the trees. You are just minutes away from Lady Bird Lake and Barton Springs Pool. Experience the live music capital of the world with ease. The home is equipped with a record player and a collection of vinyls. High-speed internet and a smart TV are included. Bicycles are provided for you to explore the neighborhood like a local. This home is perfect for families, friends, and music lovers. Feel the creative energy of Austin in every corner of this house. The bathroom features colorful tiles and a bathtub. A washer and dryer are available for your use. Discover why everyone loves Austin from this charming home base. Keep Austin Weird and stay in style. Your sunny garden escape awaits.",

            "Experience history and elegance in this Historic Townhouse in Boston. Located on a cobblestone street in Beacon Hill, this home exudes charm. The interior blends period details with modern luxury living. Features include original fireplaces, crown molding, and hardwood floors. The formal living room is perfect for entertaining guests. A chef's kitchen with custom cabinetry opens to a private courtyard. The master suite occupies an entire floor, offering ultimate privacy. Walk to the Boston Common, Public Garden, and Charles River Esplanade. Explore the rich history of the Freedom Trail just steps away. The townhouse is filled with antiques and curated artwork. Enjoy a library with a collection of classic literature. Modern amenities include central air conditioning and smart home systems. The rooftop terrace offers views of the city skyline and river. Perfect for history buffs and luxury travelers alike. Experience the sophistication of one of America's oldest cities. Concierge services can arrange private tours and dining reservations. The bathroom features marble finishes and heated floors. Live like a Boston Brahmin in this exclusive residence. A truly unforgettable stay in a landmark property. Welcome to your historic home in Boston.",

            "Create magical memories in this Spacious Family Retreat in Orlando. Located just minutes from Disney World and Universal Studios. This home is designed with families in mind, featuring themed bedrooms. The open living area is perfect for gathering together after a day at the parks. A fully equipped kitchen allows you to save on dining out. The private screened-in pool and spa are the highlight of the home. Enjoy a game room with foosball, air hockey, and a gaming console. The backyard features a playground for the little ones. Each bedroom has its own TV and comfortable bedding. The master suite offers a king bed and a large soaking tub. Located in a resort community with access to a clubhouse and water park. High-speed Wi-Fi ensures everyone stays connected. A washer and dryer make packing light easy. Strollers and high chairs are available for your convenience. Experience the magic of Orlando with all the comforts of home. Relax by the pool while the kids play safely. Close to shopping outlets and championship golf courses. This is the perfect base for your Florida family vacation. Space, comfort, and fun await you here. Book now and let the fun begin!",

            "Embrace simplicity and style in this Minimalist Studio in San Francisco. Located in the Mission District, known for its murals and food scene. The studio features a clean, modern design with clever space-saving solutions. Large windows let in abundant natural light and offer city views. The open layout includes a sleeping area, living space, and kitchenette. Furnished with high-end, functional pieces that maximize comfort. The kitchenette is equipped with a stove, fridge, and espresso machine. A sleek bathroom features a modern shower and eco-friendly toiletries. You are steps away from Dolores Park and Valencia Street boutiques. Explore the city's best burritos, bakeries, and coffee shops. Public transportation is easily accessible to take you anywhere in the city. High-speed Wi-Fi makes it a great spot for remote work. Enjoy the vibrant street life and culture of the neighborhood. The building offers a rooftop deck with views of the skyline. Secure entry and bike storage are provided. Perfect for solo travelers or couples who value design and location. Experience the innovation and creativity of San Francisco. Live efficiently without sacrificing style or comfort. Your modern urban base in the foggy city. Discover the charm of the Mission from this chic studio.",

            "Live the high life in this Ocean View Penthouse in Miami. Perched atop a luxury tower, offering 360-degree views of the ocean and city. The interior is sleek and glamorous, with white marble and glass accents. Floor-to-ceiling windows bring the stunning Miami scenery inside. The expansive terrace wraps around the unit, perfect for sunbathing or parties. A private elevator opens directly into your foyer. The gourmet kitchen features European appliances and a wine cooler. The master suite is a retreat with a spa bathroom and ocean views. Located in South Beach, you are in the center of the action. Walk to the beach, Ocean Drive, and world-famous nightclubs. The building offers a private pool, gym, and 24-hour concierge. Enjoy the ultimate VIP experience in this exclusive residence. Smart home technology controls lighting, sound, and blinds. Perfect for those who want to experience the best of Miami luxury. Watch the cruise ships pass by and the city lights sparkle at night. Host unforgettable gatherings in this show-stopping venue. Private parking and valet service are included. Indulge in the sun, sand, and style of Miami. This penthouse is the definition of luxury living. Your private palace in the sky awaits.",

            "Find your sanctuary in this Forest Hideaway in Portland. Tucked away in the lush greenery of the Pacific Northwest. The house is designed to blend seamlessly with its natural surroundings. Large windows frame views of ferns, moss, and towering trees. The interior features natural wood, stone, and cozy textiles. A wood-burning stove keeps the living room warm and inviting. The kitchen is stocked with local coffee and artisanal treats. Enjoy hiking trails in Forest Park right from your backyard. You are just a short drive from the quirky shops and donuts of downtown. The master bedroom feels like a treehouse, surrounded by canopy. Listen to the rain on the roof and the birds in the morning. A large deck offers a peaceful spot for yoga or meditation. The bathroom features a soaking tub with a view of the forest. Eco-friendly features include solar panels and rainwater harvesting. Perfect for nature lovers and those seeking a digital detox. Experience the unique \"Keep Portland Weird\" vibe. Visit the famous Japanese Garden and Rose Test Garden nearby. This home offers a peaceful retreat from the city buzz. Reconnect with nature in this magical forest setting. Welcome to your green escape in Portland.",

            "Escape to the desert in this stunning Desert Oasis in Phoenix. Surrounded by saguaro cacti and dramatic mountain landscapes. The home features a modern southwestern design with adobe accents. The backyard is a resort-style paradise with a pool and waterfall. Enjoy outdoor dining under the covered patio with a built-in BBQ. Inside, cool tile floors and high ceilings provide relief from the heat. The spacious living room features a kiva fireplace and desert views. A gourmet kitchen is perfect for preparing meals for the family. The master suite opens directly onto the pool deck. Located near Camelback Mountain for world-class hiking. Explore the desert botanical gardens and Taliesin West. Enjoy star gazing from the rooftop deck on clear desert nights. The home is equipped with smart climate control for your comfort. A game room with billiards provides indoor entertainment. Perfect for golf enthusiasts, with many courses nearby. Experience the beauty and solitude of the Sonoran Desert. Watch the spectacular desert sunsets paint the sky. Wildlife such as quail and rabbits often visit the garden. A tranquil and luxurious retreat in the Valley of the Sun. Your desert adventure begins here.",

            "Charm abounds in this historic Bungalow in Savannah. Located in the heart of the historic district, under moss-draped oaks. The home features a wide front porch with rocking chairs. Inside, you'll find original hardwood floors and 12-foot ceilings. The decor is a blend of southern traditional and eclectic vintage. A formal dining room is perfect for hosting southern suppers. The kitchen has been updated with modern appliances and farmhouse sink. Walk to the beautiful squares, river street, and Forsyth Park. Immerse yourself in the history and ghosts of Savannah. The bedrooms are spacious and feature antique four-poster beds. A private courtyard garden offers a quiet spot for tea. Enjoy the slow pace and friendly atmosphere of the south. The home is filled with books and local art. High-speed Wi-Fi and cable TV are provided. Perfect for history lovers and romantic getaways. Experience the hospitality and grace of Savannah. Visit the nearby art colleges and museums. This bungalow is a true southern belle. Step back in time and relax in style. Welcome to your charming Savannah home.",

            "Stay in royalty at this Elegant Manor in London. Located in the prestigious neighborhood of Kensington. This Victorian townhouse offers grandeur and sophistication. Features include high ceilings, intricate cornicing, and chandeliers. The drawing room is furnished with antiques and fine art. A formal dining room seats twelve for elegant dinner parties. The modern kitchen opens onto a private English garden. You are walking distance to Hyde Park, Harrods, and museums. Experience the best of London living in this exclusive home. The master suite features a dressing room and marble bathroom. Additional bedrooms are perfect for family or staff. The home includes a library and a study for quiet moments. Concierge services can arrange theater tickets and transport. Enjoy afternoon tea in the garden or the drawing room. The home is equipped with modern security and technology. Perfect for those seeking a luxurious and central London base. Explore the history and culture of the British capital. Live like a local aristocrat in this stunning manor. A truly exceptional property for the discerning traveler. Your London address awaits.",

            "Hit the slopes from this premier Ski Chalet in Denver (near resorts). While located near the city, it feels like a mountain lodge. The chalet features heavy timber construction and stone accents. A massive fireplace is the centerpiece of the great room. Floor-to-ceiling windows offer views of the distant Rocky Mountains. The kitchen is designed for feeding hungry skiers, with dual ovens. A mudroom provides ample storage for ski gear and boots. Relax in the outdoor hot tub after a day of adventure. The game room features a wet bar, pool table, and large TV. Each bedroom has a private bath and plush bedding. Located with easy access to I-70 for trips to Vail and Breckenridge. Enjoy the best of both worlds: city amenities and mountain access. The home is equipped with a sauna for post-ski recovery. High-speed internet allows you to work from the mountains. Perfect for large groups and families. Experience the outdoor lifestyle of Colorado. Hiking and biking trails are just outside your door. Watch the snow fall from the comfort of your cozy chalet. A rugged yet luxurious retreat for mountain lovers. Welcome to your base camp for adventure.",

            "Relax by the water at this Riverside Lodge in Seattle. Located on the banks of a rushing river, surrounded by forest. The lodge features a rustic yet refined design. Listen to the soothing sound of the river from every room. The living room features a river-rock fireplace and leather sofas. A large deck overhangs the water, perfect for fishing or reading. The kitchen is fully equipped for preparing fresh Pacific Northwest seafood. You are a short drive from downtown Seattle and Pike Place Market. Explore the nearby hiking trails and waterfalls. The master bedroom features a private balcony overlooking the river. Keep an eye out for eagles, herons, and salmon. The lodge is a peaceful retreat from the city rain. Enjoy a collection of board games and books by the fire. Wi-Fi is available, but you might prefer to unplug. Perfect for nature enthusiasts and those seeking solitude. Experience the moody and beautiful atmosphere of the PNW. A fire pit by the riverbank is perfect for evening gatherings. The bathroom features a jacuzzi tub with forest views. This lodge offers a unique connection to nature. Your riverside sanctuary awaits.",

            "Find your zen in this Urban Sanctuary in Los Angeles. Located in the Hollywood Hills, offering privacy and city views. The home features a mid-century modern design with clean lines. The open floor plan connects the indoors with the outdoors. A lush, tropical garden surrounds the pool and spa. The living room features a fireplace and vintage furniture. The kitchen is sleek and modern, with concrete countertops. You are minutes away from the Sunset Strip and Hollywood Bowl. Enjoy the glamour of LA while staying in a peaceful retreat. The master suite opens onto a private meditation garden. The home is filled with natural light and good energy. A yoga studio and gym are available for your wellness routine. Perfect for creatives and those looking for inspiration. The property is gated and secure for your privacy. Experience the indoor-outdoor lifestyle of Southern California. Watch the sunset over the city from your pool deck. The home is equipped with a high-end sound system. Discover the hidden staircases and trails of the hills. A stylish and serene escape in the City of Angels. Welcome to your Hollywood hideaway.",

            "Experience the charm of New England in this Vintage Farmhouse in Vermont. Surrounded by rolling hills, maple trees, and green pastures. The farmhouse dates back to the 1800s but has been lovingly restored. Features include wide-plank floors, a farmhouse sink, and a wood stove. The kitchen is the heart of the home, perfect for baking pies. Gather around the large dining table for family meals. The living room is cozy and inviting, with plenty of seating. Explore the barn and the acres of meadows and woods. You are close to charming villages, covered bridges, and ski areas. Experience the stunning fall foliage right from your porch. The bedrooms feature antique beds and handmade quilts. A vegetable garden provides fresh produce in the summer. Enjoy fresh eggs from the chickens (if you wish!). Perfect for families and those seeking a simpler life. The air is fresh and the stars are bright at night. Go apple picking, maple sugaring, or hiking nearby. The home is equipped with modern heating and Wi-Fi. A library of books and games provides entertainment. This farmhouse offers a genuine country experience. Welcome to your pastoral retreat in Vermont.",

            "Live in a work of art in this Contemporary Glass House in Vancouver. Nestled in the rainforest, this home is a masterpiece of design. Floor-to-ceiling glass walls offer immersive views of nature. The minimalist interior allows the surroundings to take center stage. Features include polished concrete floors and radiant heating. The open living area floats amongst the trees. A sleek kitchen is hidden behind seamless cabinetry. You are minutes from downtown Vancouver and Stanley Park. Experience the perfect blend of urban and natural living. The master bedroom feels like sleeping in the forest. A large terrace offers outdoor living and dining space. The home is equipped with the latest smart home technology. Perfect for design aficionados and nature lovers. Enjoy the privacy and tranquility of this unique property. Watch the mist roll through the trees and the rain fall. The bathroom features a freestanding tub with forest views. Secure and private, yet close to everything. Experience the West Coast modern lifestyle. This home has been featured in architectural magazines. Your glass sanctuary in the rainforest awaits."
        ]

        categories = ['beach', 'cabins', 'lakefront', 'views', 'castles']

        for i in range(20):
            username = f'host_{i+1}'
            email = f'host_{i+1}@example.com'
            password = 'password123'

            # Create User
            user, created = User.objects.get_or_create(username=username, email=email)
            if created:
                user.set_password(password)
                user.is_host = True
                user.save()
                self.stdout.write(f'Created user: {username}')
            else:
                self.stdout.write(f'User {username} already exists')

            # Listing Details
            title = titles[i]
            city = cities[i]
            country = countries[i]
            price = random.randint(100, 500)
            category = random.choice(categories)
            image_id = image_ids[i]
            image_url = f"https://images.unsplash.com/photo-{image_id}?auto=format&fit=crop&w=800&q=80"
            lat, lng = coordinates[i]
            description = descriptions[i]

            # Check if listing already exists
            listing, created = Listing.objects.get_or_create(
                title=title,
                defaults={
                    'host': user,
                    'price_per_night': price,
                    'room_type': 'entire_place',
                    'country': country,
                    'city': city,
                    'category': category,
                    'description': description,
                    'available_from': date.today(),
                    'available_until': date.today() + timedelta(days=365),
                    'amenities': {"wifi": True, "kitchen": True, "parking": True},
                    'latitude': lat,
                    'longitude': lng
                }
            )

            if created:
                try:
                    # Download image
                    self.stdout.write(f'Downloading image for {title}...')
                    img_temp = urllib.request.urlretrieve(image_url)
                    
                    # Save image
                    with open(img_temp[0], 'rb') as f:
                        listing.image.save(f"listing_{i+1}.jpg", ContentFile(f.read()), save=True)
                    
                    self.stdout.write(self.style.SUCCESS(f'Successfully created listing: {title}'))
                    
                    # Cleanup temp file
                    urllib.request.urlcleanup()
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Failed to create listing {title}: {e}'))
            else:
                # Update existing listing with coordinates if missing, and ALWAYS update description
                updated = False
                if listing.latitude is None or listing.longitude is None:
                    listing.latitude = lat
                    listing.longitude = lng
                    updated = True
                
                # Always update description to the new detailed one
                if listing.description != description:
                    listing.description = description
                    updated = True
                
                if updated:
                    listing.save()
                    self.stdout.write(f'Updated listing details for: {title}')
                else:
                    self.stdout.write(f'Listing {title} already up to date')

        self.stdout.write(self.style.SUCCESS('Successfully populated listings'))
