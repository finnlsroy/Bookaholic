"""Offline smoke test of the real backend logic, with Eel and num2words stubbed.
Does not start a browser or contact Open Library. Run from repository root.
"""
import sys, types, tempfile, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'backend'))
sys.modules['eel'] = types.SimpleNamespace(expose=lambda fn: fn)
sys.modules['num2words'] = types.SimpleNamespace(num2words=lambda n: str(n))
with tempfile.TemporaryDirectory() as tmp:
    os.chdir(tmp)
    os.environ['HOME'] = tmp
    os.environ['USERPROFILE'] = tmp
    from bookaholic import __main__ as api
    assert api.get_library() == {}
    assert api.get_statistics_summary()['total_books'] == 0
    b = {'metadata': {'title':'Test Book','author':'Test Author','n_pages':120,'cover_url':None,'start_date':'2026-11-01'},'subject':{'fiction':True,'genres':['Fantasy']},'rating':None}
    id_ = api.add_book(b)
    assert api.get_library()[id_]['rating'] is None
    assert api.get_top_rated() == []
    api.finish_book(id_, 5, '2026-11-03', 'Great book')
    assert api.get_library()[id_]['rating']['review'] == 'Great book'
    stats = api.get_statistics_summary()
    assert stats['total_books'] == 1 and stats['total_pages'] == 120 and stats['overall_daily_avg_pages'] == 40
    assert stats['speed_ranking'] == [id_] and api.get_top_rated() == [id_]
    api.remove_book(id_)
    assert api.get_library() == {}
print('Backend smoke test passed')
