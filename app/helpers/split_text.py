def split_text(text, max_tokens=500):
    words = text.split()
    segments = []
    current_segment = []
    
    for word in words:
        if len(current_segment) + len(word.split()) <= max_tokens:
            current_segment.append(word)
        else:
            segments.append(' '.join(current_segment))
            current_segment = [word]
    
    if current_segment:
        segments.append(' '.join(current_segment))

    return segments