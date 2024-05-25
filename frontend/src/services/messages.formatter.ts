export function formatMessage(text: string): string {
    return text
        .replace(
            /((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}/ig,
            s => '<span class="px-2 border-round bg-purple-100">' + s + '</span>'
        )
        .replace(
            /port:?\s?\S+/ig,
            s => '<span class="m-1 px-2 border-round bg-green-100">' + s + '</span>'
        );
}

export function formatMessageWithMark(text: string, pattern: string): string {
    return formatMessage(text.replace(
        new RegExp(pattern, 'ig'),
        s => '<mark>' + s + '</mark>'
    ));
}