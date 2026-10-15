from django.shortcuts import render


def games_view(request):
    games = [
        {
            "name": "BGMI",
            "category": "Battle Royale",
            "logo": "bgmi.png",
            "size": "2.1 GB",
        },
        {
            "name": "PUBG Mobile",
            "category": "Battle Royale",
            "logo": "pubg.png",
            "size": "2.4 GB",
        },
        {
            "name": "PUBG Mobile Lite",
            "category": "Battle Royale",
            "logo": "pubg-lite.png",
            "size": "600 MB",
        },
        {
            "name": "Free Fire",
            "category": "Battle Royale",
            "logo": "freefire.png",
            "size": "700 MB",
        },
        {
            "name": "Free Fire MAX",
            "category": "Battle Royale",
            "logo": "freefire-max.png",
            "size": "1.2 GB",
        },
        {
            "name": "Call of Duty Mobile",
            "category": "Action",
            "logo": "cod.png",
            "size": "2.8 GB",
        },
        {
            "name": "eFootball",
            "category": "Sports",
            "logo": "efootball.png",
            "size": "2.5 GB",
        },
        {
            "name": "Clash of Clans",
            "category": "Strategy",
            "logo": "clash-of-clans.png",
            "size": "300 MB",
        },
    ]

    # Get search query from request
    query = request.GET.get("q", "").strip().lower()

    # Filter games by name or category if query exists
    if query:
        games = [
            game
            for game in games
            if query in game["name"].lower()
            or query in game["category"].lower()
        ]

    return render(
        request, "games/games.html", {"games": games, "query": query}
    )