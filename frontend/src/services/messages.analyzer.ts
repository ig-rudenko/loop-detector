interface Message {
    message: string
}


export class MessagesAnalyzer {
    constructor(
        public messages: Message[]
    ) {}

    getVlansInfo(): Map<number, number> {
        let vlansInfo: Map<number, number> = new Map();
        for (const msg of this.messages) {
            const vlansMatch = msg.message.match(/(?<=v|vlan)\d{1,4}/ig)
            if (vlansMatch) {
                vlansMatch.forEach(value => {
                    const vid = Number(value)
                    const lastCount = vlansInfo.get(vid)
                    if (lastCount) vlansInfo.set(vid, lastCount + 1);
                    else vlansInfo.set(vid, 1);
                })
            }
        }
        return vlansInfo
    }
}