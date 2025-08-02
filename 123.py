import json
import urllib.request
import urllib.parse

class AnkiConnect:
    def __init__(self, host='localhost', port=8765):
        self.host = host
        self.port = port
        self.url = f'http://{host}:{port}'
    
    def invoke(self, action, params=None):
        """调用AnkiConnect API"""
        request_data = {
            'action': action,
            'version': 6
        }
        if params:
            request_data['params'] = params
            
        request_json = json.dumps(request_data).encode('utf-8')
        
        try:
            request = urllib.request.Request(self.url, request_json)
            request.add_header('Content-Type', 'application/json')
            
            response = urllib.request.urlopen(request)
            response_data = json.loads(response.read().decode('utf-8'))
            
            if response_data.get('error'):
                raise Exception(f"AnkiConnect错误: {response_data['error']}")
                
            return response_data.get('result')
        except Exception as e:
            print(f"API调用失败: {e}")
            return None

def copy_jlpt_cards():
    """复制NEW-JLPT卡组到print-jlpt卡组"""
    anki = AnkiConnect()
    
    print("开始复制NEW-JLPT卡组...")
    
    # 1. 检查NEW-JLPT卡组是否存在
    deck_names = anki.invoke('deckNames')
    if not deck_names or 'NEW-JLPT' not in deck_names:
        print("错误: 找不到NEW-JLPT卡组")
        return False
    
    # 2. 创建目标卡组print-jlpt
    print("创建目标卡组print-jlpt...")
    create_result = anki.invoke('createDeck', {'deck': 'print-jlpt'})
    if create_result is None:
        print("创建卡组可能失败，但可能是因为卡组已存在")
    else:
        print("卡组创建成功")
    
    # 3. 检查模板是否存在
    print("检查模板...")
    model_names = anki.invoke('modelNames')
    if not model_names or 'print-JLPT' not in model_names:
        print("警告: 找不到print-JLPT模板，将使用源模板")
        target_model = None
    else:
        target_model = 'print-JLPT'
        print(f"找到目标模板: {target_model}")
    
    # 4. 获取NEW-JLPT卡组中的所有笔记ID
    print("获取源卡组中的笔记...")
    note_ids = anki.invoke('findNotes', {'query': 'deck:"NEW-JLPT"'})
    if not note_ids:
        print("错误: NEW-JLPT卡组中没有找到笔记")
        return False
    
    print(f"找到 {len(note_ids)} 个笔记需要复制")
    
    # 5. 获取笔记详细信息
    print("获取笔记详细信息...")
    notes_info = anki.invoke('notesInfo', {'notes': note_ids})
    if not notes_info:
        print("错误: 无法获取笔记信息")
        return False
    
    # 6. 复制笔记
    print("开始复制笔记...")
    success_count = 0
    error_count = 0
    
    for i, note_info in enumerate(notes_info):
        try:
            # 准备新笔记数据
            new_note = {
                'deckName': 'print-jlpt',
                'modelName': target_model if target_model else note_info['modelName'],
                'fields': note_info['fields'],
                'tags': note_info['tags']
            }
            
            # 添加新笔记
            result = anki.invoke('addNote', {'note': new_note})
            if result:
                success_count += 1
                if (i + 1) % 50 == 0:  # 每50个笔记显示一次进度
                    print(f"已处理 {i + 1}/{len(notes_info)} 个笔记")
            else:
                error_count += 1
                print(f"复制笔记失败: {note_info.get('noteId', 'unknown')}")
                
        except Exception as e:
            error_count += 1
            print(f"处理笔记时出错: {e}")
    
    print(f"\n复制完成!")
    print(f"成功复制: {success_count} 个笔记")
    print(f"失败: {error_count} 个笔记")
    print(f"总计: {len(notes_info)} 个笔记")
    
    # 7. 如果指定了新模板，尝试批量更改模板
    if target_model and success_count > 0:
        print(f"\n应用模板 {target_model}...")
        try:
            # 获取新卡组中的笔记
            new_note_ids = anki.invoke('findNotes', {'query': 'deck:"print-jlpt"'})
            if new_note_ids:
                # 批量更改模板
                change_result = anki.invoke('changeModel', {
                    'notes': new_note_ids,
                    'modelName': target_model
                })
                if change_result:
                    print("模板应用成功")
                else:
                    print("模板应用可能失败")
        except Exception as e:
            print(f"应用模板时出错: {e}")
    
    return success_count > 0

def main():
    """主函数"""
    print("NEW-JLPT卡组复制工具")
    print("=" * 40)
    
    try:
        # 检查AnkiConnect连接
        anki = AnkiConnect()
        version = anki.invoke('version')
        if version:
            print(f"AnkiConnect版本: {version}")
        else:
            print("错误: 无法连接到AnkiConnect")
            print("请确保:")
            print("1. Anki正在运行")
            print("2. AnkiConnect插件已安装并启用")
            return
        
        # 开始复制
        success = copy_jlpt_cards()
        
        if success:
            print("\n复制操作完成! 请检查Anki中的print-jlpt卡组")
        else:
            print("\n复制操作失败，请检查错误信息")
            
    except KeyboardInterrupt:
        print("\n操作被用户取消")
    except Exception as e:
        print(f"\n程序出错: {e}")

if __name__ == "__main__":
    main()