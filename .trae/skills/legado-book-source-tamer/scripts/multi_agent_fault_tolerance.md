# 多智能体容错机制设计

## 核心设计原则
```失败 → 分类 → 重试 → 降级 → 询问用户```

## 一、失败检测与分类

### 1. 失败类型

| 类型 | 检测方式 | 示例 |
|------|----------|------|
| **网络失败** | 返回空结果/异常 | 页面抓取超时 |
| **解析失败** | 规则匹配为空 | CSS选择器找不到元素 |
| **结构变化** | 返回格式不符预期 | 网站改版 |
| **反爬拦截** | 返回验证页/403 | 需要验证码 |

### 2. 关键程度分级

```python
CRITICAL = ['search', 'detail', 'toc', 'content']  # 必须成功
OPTIONAL = ['explore', 'cover', 'intro']           # 可选功能
```

## 二、容错策略

### 策略1：自动重试（推荐）

```
智能体失败 → 等待1秒 → 重试 → 最多3次 → 仍失败则标记
```

### 策略2：降级处理

```
正文页分析失败 → 尝试备用选择器 → 尝试通用规则 → 标记为"需人工处理"
```

### 策略3：部分成功继续

```
5个智能体中4个成功 → 生成部分书源 → 标记缺失部分 → 用户可手动补充
```

## 三、实现方案

### 方案A：主线程收集结果，失败则重试

```python
def analyze_with_retry(agents, max_retries=3):
    results = {}
    failed = []
    
    # 第一轮：并行执行所有智能体
    for agent in agents:
        result = agent.execute()
        if result.success:
            results[agent.name] = result.data
        else:
            failed.append(agent)
    
    # 第二轮：重试失败的智能体
    for retry in range(max_retries):
        if not failed:
            break
        still_failed = []
        for agent in failed:
            result = agent.execute()
            if result.success:
                results[agent.name] = result.data
            else:
                still_failed.append(agent)
        failed = still_failed
    
    # 返回结果和失败列表
    return results, failed
```

### 方案B：关键失败则询问用户

```python
def handle_failures(results, failed, critical_list):
    critical_failures = [f for f in failed if f.name in critical_list]
    
    if critical_failures:
        # 关键智能体失败，询问用户
        message = f"以下关键分析失败：{[f.name for f in critical_failures]}"
        user_choice = ask_user(message, options=[
            "重试",
            "继续生成（部分功能缺失）",
            "放弃"
        ])
        
        if user_choice == "重试":
            return retry_agents(critical_failures)
        elif user_choice == "继续生成":
            return generate_partial_source(results)
        else:
            return None
    else:
        # 非关键失败，继续生成
        return generate_source_with_warnings(results, failed)
```

## 四、实际代码示例

```python
import asyncio
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class AgentResult:
    name: str
    success: bool
    data: Optional[dict]
    error: Optional[str]

class MultiAgentAnalyzer:
    CRITICAL = ['search', 'detail', 'toc', 'content']
    MAX_RETRIES = 3
    
    def __init__(self, agents: List):
        self.agents = agents
        self.results = {}
        self.failed = []
    
    async def run_all(self) -> tuple:
        """并行执行所有智能体，返回(成功结果, 失败列表)"""
        
        # 第一轮并行执行
        tasks = [agent.analyze() for agent in self.agents]
        first_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, result in enumerate(first_results):
            if isinstance(result, Exception):
                self.failed.append((self.agents[i], str(result)))
            elif result.success:
                self.results[result.name] = result.data
            else:
                self.failed.append((self.agents[i], result.error))
        
        # 重试失败的智能体
        await self._retry_failed()
        
        return self.results, self.failed
    
    async def _retry_failed(self):
        """重试失败的智能体"""
        for retry in range(self.MAX_RETRIES):
            if not self.failed:
                break
            
            still_failed = []
            for agent, error in self.failed:
                try:
                    result = await agent.analyze()
                    if result.success:
                        self.results[result.name] = result.data
                    else:
                        still_failed.append((agent, result.error))
                except Exception as e:
                    still_failed.append((agent, str(e)))
            
            self.failed = still_failed
            
            if self.failed:
                await asyncio.sleep(1)  # 等待后重试
    
    def get_critical_failures(self) -> List:
        """获取关键失败项"""
        return [(a, e) for a, e in self.failed if a.name in self.CRITICAL]
    
    def can_generate_partial(self) -> bool:
        """判断是否可以生成部分书源"""
        # 至少要有详情和目录
        return 'detail' in self.results and 'toc' in self.results
```

## 五、用户交互流程

```
┌─────────────────────────────────────────────────────────────┐
│                    多智能体并行分析                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  第一轮并行执行：Agent1 ✓  Agent2 ✓  Agent3 ✗  Agent4 ✓     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  检测失败：Agent3 失败（正文页分析）                          │
│  判断关键程度：CRITICAL（必须成功）                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  自动重试（最多3次）                                         │
│  重试1：失败 → 重试2：失败 → 重试3：成功 ✓                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  全部成功 → 生成完整书源                                      │
└─────────────────────────────────────────────────────────────┘
```

### 实际处理流程

```
并行执行所有智能体
       ↓
   收集结果
       ↓
┌──────────────────┐
│ 有失败？         │──否──→ 生成完整书源
└──────────────────┘
       │是
       ↓
┌──────────────────┐
│ 是关键失败？     │──否──→ 标记警告，生成部分书源
└──────────────────┘
       │是
       ↓
┌──────────────────┐
│ 自动重试3次      │──成功→ 生成完整书源
└──────────────────┘
       │失败
       ↓
┌──────────────────┐
│ 询问用户：       │
│ 1. 继续重试      │
│ 2. 部分生成      │
│ 3. 放弃          │
└──────────────────┘
```


## 六、失败后的处理选项

| 失败情况 | 选项1 | 选项2 | 选项3 |
|----------|-------|-------|-------|
| 单个非关键失败 | 自动跳过，继续生成 | 重试 | 询问用户 |
| 单个关键失败 | 自动重试3次 | 询问用户 | 放弃 |
| 多个失败 | 串行重试 | 部分生成 | 放弃 |
| 全部失败 | 报告错误 | 切换方案 | 放弃 |

## 七、最佳实践

1. **先并行，后重试** - 第一轮并行执行，失败的重试时可以串行
2. **区分关键程度** - 关键失败必须处理，非关键可以跳过
3. **保留错误信息** - 记录失败原因，便于调试
4. **用户可介入** - 关键失败时询问用户决策
5. **部分成功也输出** - 即使有失败，也输出已成功的部分
