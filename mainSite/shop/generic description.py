from random import choice

def replace_placeholder(input_str, placeholder, replacement):
    return input_str.replace(placeholder, replacement)


dog_treat_descriptions = [
    "A delicious reward for our four-legged companions, dog treats are specially crafted to delight brand_name's furry friends. These bite-sized morsels are more than just snacks; they're gestures of affection and connection. Designed with a perfect blend of flavors, textures, and nutritional value, brand_name's dog treats offer a delightful pause in the day, a moment when tails wag and eyes light up. Whether used as training incentives, bonding tools, or simply to celebrate the everyday moments, these treats reflect brand_name's commitment to canine well-being. Each treat is a testament to the joy that dogs bring into our lives, and they're created with the same care and attention that we provide to our beloved pets. From chewy delights to crunchy bites, brand_name's range of dog treats caters to a variety of preferences, ensuring that every dog finds a treat that tantalizes their taste buds and warms their hearts. With an emphasis on quality ingredients and thoughtful formulations, brand_name's treats stand as a testament to the strong bond between humans and their loyal companions, where a simple treat can convey an abundance of love and appreciation.",

    "Indulge your pup's senses with brand_name's gourmet dog treats, a symphony of flavors that dance on their taste buds. These delectable creations are a blend of culinary expertise and tail-wagging enthusiasm, making each bite a moment of pure delight. Crafted with a medley of carefully chosen ingredients, these treats offer a perfect balance of taste and nutrition. Whether it's the satisfying crunch or the savory goodness, brand_name's treats turn ordinary moments into joyful celebrations. Share the joy of snack time with your loyal companion and witness the happiness that these treats bring to their day. With each treat, you're nurturing not only their palate but also the special bond you share.",

    "Elevate your dog's day with brand_name's artisanal dog treats, handcrafted with a touch of canine joy. Each treat is a masterpiece of flavor, a canvas of taste that sparks tails to wag and noses to twitch in anticipation. Made from thoughtfully sourced ingredients, these treats are a heartfelt expression of care for your furry friend's well-being. As your dog nibbles on these treasures, they'll experience a burst of happiness that transcends the ordinary. The bond you share finds its perfect companion in these treats, where simple moments become memorable through shared joy and a treat that's as extraordinary as your loyal companion.",

    "Unleash the extraordinary with brand_name's premium dog treats – a culinary journey designed exclusively for your beloved pup. These treats are more than a snack; they're an invitation to savor life's little pleasures. With a harmonious blend of flavors and textures, each bite is a crescendo of happiness that resonates in every wagging tail. These treats are a reminder of the unspoken connection you share, where a single look or a joyful bark speaks volumes. Delight your furry friend with a treat that mirrors their importance in your life, and let each moment of shared joy be a testament to the love and devotion that makes your bond truly special.",

    "Embark on a flavor-filled journey with brand_name's dog treats, a passport to happiness for your furry explorer. Crafted with a blend of exotic ingredients and boundless care, these treats are a passport to joy that transcends language barriers. With each nibble, your dog ventures into a world of taste, a treasure trove of delight waiting to be discovered. Whether it's the satisfying crunch or the burst of flavors, these treats are an ode to the adventurer in your loyal companion.",

    "Introducing brand_name's Delightful Bites – a symphony of taste that orchestrates a ballet of joy in every chew. Each treat is a note of happiness, played to perfection with a blend of carefully chosen ingredients. As your pup enjoys these bites, they're not just savoring flavors; they're celebrating life's moments. With every tail wag and every excited bark, they're sharing the language of love and appreciation.",

    "Unlock the secret to a wagging tail with brand_name's Tail-Wagging Delights – treats that speak the language of canine happiness. These treats are like a warm hug in every bite, a gesture of care that wraps your pup in a blanket of joy. Made from the heart and designed to dazzle the palate, each treat is a celebration of the bond you share. As your dog savors the taste, their tail becomes a painter's brush, creating strokes of delight in the air.",

    "Let your pup indulge in brand_name's Timeless Classics – treats that bring nostalgia and joy together in a single bite. These treats capture the essence of cherished moments, where the warmth of your companionship melds with the satisfying crunch of each bite. With a dash of love and a sprinkle of delight, every nibble becomes a memory in the making, reminding both of you that simple pleasures are the most extraordinary.",
]
placeholder = "brand_name"
# Input from the user
replacement = input("Enter the replacement word: ")

# Perform the replacement
modified_description = replace_placeholder(choice(dog_treat_descriptions), placeholder, replacement)

# Print the modified description
print(modified_description)