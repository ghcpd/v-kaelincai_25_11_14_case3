import sys, json
from pathlib import Path

def main(pre_path, post_path, out_md):
    pre = json.loads(open(pre_path).read())
    post = json.loads(open(post_path).read())
    lines = []
    lines.append('# UI/UX Evaluation Compare Report')
    lines.append('')
    lines.append('## Summary Metrics')
    lines.append('| Metric | Before | After | Delta |')
    lines.append('|---|---:|---:|---:|')
    def n(v):
        return v
    spacing_pre = pre.get('spacing_stddev', 0)
    spacing_post = post.get('spacing_stddev', 0)
    icons_pre = pre.get('icons_ok', False)
    icons_post = post.get('icons_ok', False)
    lines.append(f'|Spacing StdDev|{spacing_pre:.3f}|{spacing_post:.3f}|{spacing_post - spacing_pre:+.3f}|')
    lines.append(f'|Icons Aligned|{icons_pre}|{icons_post}|{icons_post != icons_pre}|')
    lines.append(f'|Title Count|{pre.get("title_count")}|{post.get("title_count")}|{post.get("title_count") - pre.get("title_count")}|')

    # DOM tree diffs
    pre_titles = pre.get('titles', [])
    post_titles = post.get('titles', [])
    diffs = [t for t in post_titles if t not in pre_titles]
    lines.append('\n## DOM Diffs')
    lines.append(f'- New titles (in After, not in Before): {diffs}')

    # Recommendations
    lines.append('\n## Notes and Recommendations')
    if spacing_post < spacing_pre:
        lines.append('- ✅ Spacing standard deviation decreased, layout more consistent.')
    else:
        lines.append('- ⚠️ Spacing variance increased; review improved layout rules')
    if icons_post and not icons_pre:
        lines.append('- ✅ Icons aligned: improved baseline vertical alignment')
    lines.append('\n## Detailed pre/post JSON')
    lines.append('\n**Before**')
    lines.append('```json')
    lines.append(json.dumps(pre, indent=2))
    lines.append('```')
    lines.append('\n**After**')
    lines.append('```json')
    lines.append(json.dumps(post, indent=2))
    lines.append('```')

    Path(out_md).write_text('\n'.join(lines), encoding='utf8')

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('usage: compare_results.py pre.json post.json out.md')
        sys.exit(2)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
