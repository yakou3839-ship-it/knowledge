### 前言

![image-20260807112451392](assets/image-20260807112451392.png)

### prompt engineering

> 用户给大模型的话，门槛低，大模型能力变强，所以过时了

### context engineering

> 上下文不是无上限，需要精心设计context，但是能力有上限

几个非常经典的技术：

- 上下文压缩
- 动态检索外部资料
- 渐进式披露

### harness engineering

> 大模型就像是野马，harness就是控制马的工具（让大模型不那么扩散思维），可以抽象为harness=agent-model

具体例子claude code：

claude.md、可使用的工具、定时调度机制等都是harness

> harness engineering就是研究如何构建与设计harness的技术，除了大模型不研究，别的都研究。
>
> 并不是一个新的技术，而是一个驾驭框架系统，比如说claude code用paner、generate与evaluator三个agent之间的合作也算是一种harness engineering