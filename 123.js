// 转换平假名为罗马音
function convertHiraganaToRomaji(hiragana) {
    
    const hiraganaToRomaji = {
        // 基本假名
        'あ': 'a', 'い': 'i', 'う': 'u', 'え': 'e', 'お': 'o',
        'か': 'ka', 'き': 'ki', 'く': 'ku', 'け': 'ke', 'こ': 'ko',
        'が': 'ga', 'ぎ': 'gi', 'ぐ': 'gu', 'げ': 'ge', 'ご': 'go',
        'さ': 'sa', 'し': 'shi', 'す': 'su', 'せ': 'se', 'そ': 'so',
        'ざ': 'za', 'じ': 'ji', 'ず': 'zu', 'ぜ': 'ze', 'ぞ': 'zo',
        'た': 'ta', 'ち': 'chi', 'つ': 'tsu', 'て': 'te', 'と': 'to',
        'だ': 'da', 'ぢ': 'ji', 'づ': 'zu', 'で': 'de', 'ど': 'do',
        'な': 'na', 'に': 'ni', 'ぬ': 'nu', 'ね': 'ne', 'の': 'no',
        'は': 'ha', 'ひ': 'hi', 'ふ': 'fu', 'へ': 'he', 'ほ': 'ho',
        'ば': 'ba', 'び': 'bi', 'ぶ': 'bu', 'べ': 'be', 'ぼ': 'bo',
        'ぱ': 'pa', 'ぴ': 'pi', 'ぷ': 'pu', 'ぺ': 'pe', 'ぽ': 'po',
        'ま': 'ma', 'み': 'mi', 'む': 'mu', 'め': 'me', 'も': 'mo',
        'や': 'ya', 'ゆ': 'yu', 'よ': 'yo',
        'ら': 'ra', 'り': 'ri', 'る': 'ru', 'れ': 're', 'ろ': 'ro',
        'わ': 'wa', 'ゐ': 'wi', 'ゑ': 'we', 'を': 'wo', 'ん': 'n',
        
        // 拗音
        'きゃ': 'kya', 'きゅ': 'kyu', 'きょ': 'kyo',
        'ぎゃ': 'gya', 'ぎゅ': 'gyu', 'ぎょ': 'gyo',
        'しゃ': 'sha', 'しゅ': 'shu', 'しょ': 'sho',
        'じゃ': 'ja', 'じゅ': 'ju', 'じょ': 'jo',
        'ちゃ': 'cha', 'ちゅ': 'chu', 'ちょ': 'cho',
        'にゃ': 'nya', 'にゅ': 'nyu', 'にょ': 'nyo',
        'ひゃ': 'hya', 'ひゅ': 'hyu', 'ひょ': 'hyo',
        'びゃ': 'bya', 'びゅ': 'byu', 'びょ': 'byo',
        'ぴゃ': 'pya', 'ぴゅ': 'pyu', 'ぴょ': 'pyo',
        'みゃ': 'mya', 'みゅ': 'myu', 'みょ': 'myo',
        'りゃ': 'rya', 'りゅ': 'ryu', 'りょ': 'ryo',
        
        // 特殊记号
        'ー': '-', '・': '・'
    };

    if (!hiragana) return '';
    
    let result = '';
    let i = 0;
    
    while (i < hiragana.length) {
        let converted = false;
        
        // 处理促音 (っ)
        if (hiragana[i] === 'っ' && i + 1 < hiragana.length) {
            const nextChar = hiragana[i + 1];
            const nextRomaji = hiraganaToRomaji[nextChar];
            if (nextRomaji) {
                result += nextRomaji[0]; // 重复辅音
                i++;
                continue;
            }
        }
        
        // 检查拗音 (2字符)
        if (i + 1 < hiragana.length) {
            const twoChar = hiragana.slice(i, i + 2);
            if (hiraganaToRomaji[twoChar]) {
                result += hiraganaToRomaji[twoChar];
                i += 2;
                converted = true;
            }
        }
        
        // 检查单个字符
        if (!converted) {
            const oneChar = hiragana[i];
            if (hiraganaToRomaji[oneChar]) {
                // 处理特殊的 'n' 规则
                if (oneChar === 'ん') {
                    // 如果后面是 y, w 或元音，使用 n'
                    if (i + 1 < hiragana.length) {
                        const next = hiragana[i + 1];
                        if ('あいうえおやゆよわをん'.includes(next) || next === 'y' || next === 'w') {
                            result += "n'";
                        } else {
                            result += 'n';
                        }
                    } else {
                        result += 'n';
                    }
                } else {
                    result += hiraganaToRomaji[oneChar];
                }
                i++;
                converted = true;
            }
        }
        
        // 如果没有转换，保持原字符
        if (!converted) {
            result += hiragana[i];
            i++;
        }
    }
    
    // 清理多余的空格和特殊字符
    return result.replace(/\s+/g, '').toLowerCase();
}


const romaji = convertHiraganaToRomaji("かどかわ")
console.log(romaji)