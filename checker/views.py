from django.shortcuts import render
from django.http import JsonResponse
from .models import Brand, Device, Game, CompatibilityCheck

def index(request):
    """Render the main page."""
    return render(request, 'checker/index.html')

def api_brands(request):
    """Returns brands list expected by frontend JS."""
    brands = Brand.objects.all().order_by('brand_name')
    data = []
    for b in brands:
        data.append({
            'brand_id': b.brand_id,
            'name': b.brand_name
        })
    return JsonResponse(data, safe=False)

def api_devices(request):
    """Returns devices filtered by brand_id with 'model' key for JS compatibility."""
    brand_id = request.GET.get('brand_id')
    if brand_id:
        devices = Device.objects.filter(brand_id=brand_id)
        data = []
        for d in devices:
            data.append({
                'device_id': d.device_id,
                'model': d.device_name,
                'segment': d.segment,
                'chipset': d.chipset,
                'antutu_score': d.antutu_score
            })
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)

def api_versions(request):
    """Returns all available versions/games in the structure expected by frontend JS."""
    games = Game.objects.all().order_by('name')
    data = []
    for g in games:
        data.append({
            'version': g.current_version.replace("BGMI ", "").replace("v", "").strip(),
            'min_antutu': g.min_antutu_score,
            'fps_label': g.target_fps,
            'download_url': g.download_url or '#'
        })
    return JsonResponse(data, safe=False)

def api_check_device(request, device_id):
    """Calculates compatibility based on selected device ID."""
    try:
        device = Device.objects.get(pk=device_id)
    except Device.DoesNotExist:
        return JsonResponse({'error': 'Device not found.'}, status=404)

    antutu = device.antutu_score
    all_versions = list(Game.objects.all().order_by('min_antutu_score'))
    
    versions_data = []
    supported_versions = []
    
    for g in all_versions:
        v_num = g.current_version.replace("BGMI ", "").replace("v", "").strip()
        supported = antutu >= g.min_antutu_score
        v_info = {
            'version': v_num,
            'min_antutu': g.min_antutu_score,
            'fps_label': g.target_fps,
            'download_url': g.download_url or '#',
            'supported': supported
        }
        versions_data.append(v_info)
        if supported:
            supported_versions.append(v_info)

    # Determine best match (highest supported version)
    best = supported_versions[-1] if supported_versions else None
    
    # Mark best in versions data
    for v in versions_data:
        v['isBest'] = (best and v['version'] == best['version'])

    # Find next upgrade if there's any unsupported version above current max
    next_upgrade = None
    for v in versions_data:
        if not v['supported']:
            next_upgrade = {
                'version': v['version'],
                'min_antutu': v['min_antutu'],
                'gap': v['min_antutu'] - antutu
            }
            break

    return JsonResponse({
        'antutu': antutu,
        'device': {
            'brand': device.brand.brand_name,
            'model': device.device_name,
            'chipset': device.chipset
        },
        'recommended': best,
        'next_upgrade': next_upgrade,
        'versions': versions_data
    })

def api_check_score(request):
    """Calculates compatibility based on manually entered AnTuTu score."""
    try:
        antutu = int(request.GET.get('antutu', 0))
    except ValueError:
        return JsonResponse({'error': 'Invalid score.'}, status=400)

    all_versions = list(Game.objects.all().order_by('min_antutu_score'))
    
    versions_data = []
    supported_versions = []
    
    for g in all_versions:
        v_num = g.current_version.replace("BGMI ", "").replace("v", "").strip()
        supported = antutu >= g.min_antutu_score
        v_info = {
            'version': v_num,
            'min_antutu': g.min_antutu_score,
            'fps_label': g.target_fps,
            'download_url': g.download_url or '#',
            'supported': supported
        }
        versions_data.append(v_info)
        if supported:
            supported_versions.append(v_info)

    best = supported_versions[-1] if supported_versions else None
    
    for v in versions_data:
        v['isBest'] = (best and v['version'] == best['version'])

    next_upgrade = None
    for v in versions_data:
        if not v['supported']:
            next_upgrade = {
                'version': v['version'],
                'min_antutu': v['min_antutu'],
                'gap': v['min_antutu'] - antutu
            }
            break

    return JsonResponse({
        'antutu': antutu,
        'device': None,
        'recommended': best,
        'next_upgrade': next_upgrade,
        'versions': versions_data
    })