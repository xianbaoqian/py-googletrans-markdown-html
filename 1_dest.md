---
标题：“是什么让对话代理有用？”
缩略图：/blog/assets/dialog-agents/thumbnail.png
---


# 是什么让对话代理有用？
## ChatGPT 背后的技术：RLHF、IFT、CoT、红队等

<div class="blog-metadata">
    <small>2023 年 1 月 24 日发布。</small>
    <a target="_blank" class="btn no-underline text-sm mb-5 font-sans" href="https://github.com/huggingface/blog/blob/main/rlhf.md">
        在 GitHub 上更新
    </a>
</div>
<div class="author-card">
    <a href="/nazneen">
        <img class="avatar avatar-user" src="https://avatars.githubusercontent.com/u/3278583?v=4?w=200&h=200&f=face" title="Gravatar">
        <div class="bfc">
            <code>纳兹宁</code>
            <span class="fullname">纳兹宁·拉贾尼</span>
        </div>
    </a>
    <a href="/natolambert">
        <img class="avatar avatar-user" src="https://avatars.githubusercontent.com/u/10695622?v=4?w=200&h=200&f=face" title="Gravatar">
        <div class="bfc">
            <code>纳托兰伯特</code>
            <span class="fullname">弥敦道兰伯特</span>
        </div> </a>
    <a href="/VictorSanh">
        <img class="avatar avatar-user" src="https://aeiljuispo.cloudimg.io/v7/https://s3.amazonaws.com/moonup/production/uploads/1590600248871-noauth.jpeg?w=200&h=200&f=face" title="Gravatar">
        <div class="bfc">
            <code>VictorSanh</code>
            <span class="fullname">维克多山</span>
        </div>
    </a>
    <a href="/ThomWolf">
        <img class="avatar avatar-user" src="https://avatars.githubusercontent.com/u/7353373?v=4?w=200&h=200&f=face" title="Gravatar">
        <div class="bfc">
            <code>汤姆狼</code>
            <span class="fullname">托马斯·沃尔夫</span>
        </div>
    </a>
 </div>

几周前，ChatGPT 出现并在公共讨论中推出了一组晦涩的首字母缩略词：RLHF、SFT、IFT、CoT 等，所有这些都归功于 ChatGPT 的成功。这些晦涩的首字母缩略词是什么？为什么它们如此重要？我们调查了关于这些主题的所有重要论文，以对这些作品进行分类，总结已经完成的工作，并分享有待展示的内容。

让我们先来看看基于语言模型的会话代理的前景。 ChatGPT 并不是第一个，事实上很多组织在 OpenAI 之前就发布了他们的语言模型对话代理，包括 [Meta 的 BlenderBot](https://arxiv.org/abs/2208.03188)，[Google 的 LaMDA](https://arxiv.org /abs/2201.08239)，[DeepMind 的麻雀](https://arxiv.org/abs/2209.14375)，以及 [Anthropic 的助手](https://arxiv.org/abs/2204.05862)完美归因也称为 Claude_）。一些团体还宣布了他们构建开源聊天机器人的计划，并公开分享了路线图（[LAION 的 Open Assistant](https://github.com/LAION-AI/Open-Assistant)）；其他人肯定正在这样做，但尚未宣布。

下表根据公开访问、训练数据、模型架构和评估方向的详细信息对这些 AI 聊天机器人进行了比较。 ChatGPT 没有记录在案，因此我们改为分享有关 InstructGPT 的详细信息，这是一个来自 OpenAI 的指令微调模型，据信它是 ChatGPT 的基础。

| |拉姆达 | BlenderBot 3 |麻雀 |聊天GPT/ InstructGPT |助理|
| --- | --- | --- | --- | --- | --- |
| **组织** |谷歌 |元 |深度思维 |开放人工智能 |人择 |
| **访问** |关闭 |打开|关闭 |有限 |关闭 |
| **尺寸** | 137B | 175B | 70B | 175B | 52B |
| **预训练<br>基础模型** |未知 |选择 |龙猫 | GPT-3.5 |未知 |
| **预训练语料库大小**（# tokens）| 2.81T | 180B | 1.4T |未知 | 400B |
| **模型可以<br>访问网络** | ✔ | ✔ | ✔ | ✖️ | ✖️ |
| **监督<br>微调** | ✔ | ✔ | ✔ | ✔ | ✔ |
| **微调<br>数据大小** |质量：6.4K<br>安全性：8K<br>接地性：4K<br>IR：49K | 20 个 NLP 数据集，从 18K 到 1.2M |未知 | 12.7K（对于 InstructGPT，对于 ChatGPT 可能更多）| 150K + LM 生成的数据 |
| **左高频** | ✖️ | ✖️ | ✔ | ✔ | ✔ |
| **手写的安全规则** | ✔ | ✖️ | ✔ | ✖️ | ✔ |
| **评价标准** | 1. 质量（敏感性、特异性、趣味性）<br>2.安全（包括偏见） 3. 接地气 | 1、质量（参与度、知识运用）<br>2。安全性（毒性、偏倚）| 1.对齐（有帮助，无害，正确）<br>2。证据（来自网络）<br>3。违反规则<br>4。偏见和刻板印象<br>5。守信 | 1. 对齐（有帮助、无害、真实）<br>2.偏见 | 1. 对齐（有帮助、无害、诚实）<br>2.偏见 |
| **用于数据标注的众包平台**|美国供应商 |亚马逊 MTurk |未知 |升级和扩展 AI | Surge AI、Amazon MTurk 和 Upwork |

我们观察到，尽管在训练数据、模型和微调方面存在许多差异，但也存在一些共性。上述所有聊天机器人的一个共同目标是 *instruction*c*tion following ,* 即遵循用户指定的指令。例如，指导 ChatGPT 写一首关于微调的诗。

![ChatGPT 指令示例](assets/dialog-agents/chatgpt-example.png)

### *************************************************** ***************************************************来自预测文本按照以下说明：*************************************************** ***************************************************

通常，基础模型的语言建模目标不足以让模型学会以有用的方式遵循用户的指示。模型创建者使用 **指令微调 (IFT)**，除了情感、文本分类、摘要等经典 NLP 任务外，它还涉及在非常多样化的任务集上对基本模型的书面说明进行微调。这些指令演示由三个主要部分组成——指令、输入和输出。输入是可选的，一些任务只需要指令，例如上面使用 ChatGPT 的示例中的开放式生成。存在时的输入和输出形成一个*实例*。给定指令可以有多个输入和输出实例。示例见下文（摘自 [Wang 等人，'22]）。

![说明和实例示例](assets/dialog-agents/ift.png)

IFT 的数据通常是人工编写的指令和使用语言模型引导的指令实例的集合。对于引导程序，LM 在带有示例的几个镜头设置中被提示（如上图所示），并指示生成新的指令、输入和输出。在每一轮中，模型都会收到从人工编写的和模型生成的样本中选择的样本。人类和模型对创建数据集的贡献是一个范围；见下图。

![IFT 频谱](assets/dialog-agents/ift-spectrum.png)

一方面是纯模型生成的 IFT 数据集，例如 Unnatural Instructions（[Honovich et al., '22](https://arxiv.org/abs/2212.09689)），另一方面是社区的大量努力- 超自然指令中的精心制作的指令（[Wang 等人，'22]（https://arxiv.org/abs/2204.07705））。在这两者之间的工作是使用一小组高质量的种子数据集，然后进行引导，例如自我指导（[Wang et al., 22](https://arxiv.org/pdf/2212.10560.pdf)）。为 IFT 整理数据集的另一种方法是将现有的高质量众包 NLP 数据集用于各种任务（包括提示），并使用统一模式或不同模板将其转换为指令。这一系列工作包括 T0（[Sanh 等人，'22]（https://arxiv.org/pdf/2110.08207.pdf））、自然指令数据集（[Mishra 等人，'22]（https： //arxiv.org/pdf/2104.08773.pdf)), FLAN LM ([Wei et al., '22](https://arxiv.org/pdf/2109.01652.pdf)), 和 OPT-IML ( [Iyer 等人，'22](https://arxiv.org/pdf/2212.12017.pdf)）。

### 安全地遵循指示

然而，经过指令微调的 LM 可能并不总是生成 ******** 有帮助的 ******** 和 ********** 安全的响应。***** ***** 这种行为的例子包括通过总是给出无益的回应来逃避，例如“对不起，我不明白。 ” 或对敏感主题的用户输入生成不安全的响应。为了减轻这种行为，模型开发人员使用**监督微调 (SFT)**，在高质量的人类注释数据上微调基础语言模型，以提高有用性和无害性。例如，请参阅下表，摘自 Sparrow 论文（附录 F）。

SFT 和 IFT 联系非常紧密。指令调整可以看作是监督微调的一个子集。在最近的文献中，SFT 阶段经常用于安全主题，而不是在 IFT 之后完成的指令特定主题。将来，这种分类和描述应该成熟为更清晰的用例和方法。

![汉字安全规则](assets/dialog-agents/rules.png)

谷歌的 LaMDA 还根据一组规则（附录 A）在带有安全注释的对话数据集上进行了微调。这些规则通常由模型创建者预先定义和开发，涵盖范围广泛的主题，包括伤害、歧视、错误信息。

### 微调模型

另一方面，Open AI 的 InstructGPT、DeepMind 的 Sparrow 和 Anthropic 的 Constitutional AI 在称为**人类反馈强化学习 (RLHF) 的设置中使用人类偏好注释。**在 RLHF 中，一组模型响应根据人类反馈（例如，选择一个比另一个更受欢迎的文本简介）。接下来，根据这些带注释的响应训练偏好模型，以返回 RL 优化器的标量奖励。最后，通过强化学习训练对话代理来模拟偏好模型。有关更多详细信息，请参阅我们之前关于 RLHF 的[博文](https://huggingface.co/blog/rlhf)。

**思想链 (CoT)** 提示（[Wei 等人，'22](https://arxiv.org/abs/2201.11903)）是指令演示的一种特殊情况，它通过引发步骤生成输出- 来自对话代理的逐步推理。使用 CoT 微调的模型使用带有逐步推理的人工注释的指令数据集。这是著名提示的由来，***************************[让我们一步步思考](https://arxiv.org /abs/2205.11916)***************************。下面的示例取自 [Chung 等人，'22](https://arxiv.org/pdf/2210.11416.pdf)。橙色突出显示指令，粉色显示输入和输出，蓝色是 CoT 推理。

![CoT插图](assets/dialog-agents/cot.png)
如 [Chung 等人，'22](https://arxiv.org/pdf/2210.11416.pdf) 中所述，使用 CoT 微调的模型在涉及常识、算术和符号推理的任务上表现得更好。

CoT 微调也显示出对无害性非常有效（有时比 RLHF 做得更好），而模型不会回避并生成“抱歉，我无法回答这个问题”，对于敏感的提示，如 [Bai 等人所示] .,'22](https://www.anthropic.com/constitutional.pdf)。有关更多示例，请参见其论文的附录 D。

![比较 CoT 和 RLHF](assets/dialog-agents/rlhf.png)

## 要点：

1. 与预训练数据相比，您只需要非常小的一部分数据来进行指令微调（几百个数量级）。
2. 有监督的微调使用人工注释使模型输出更安全和有用。
3. CoT 微调提高了模型在需要逐步思考的任务上的性能，并使它们在敏感话题上不那么回避。

## 对话代理的后续步骤

这个博客总结了许多关于使对话代理有用的现有工作。但仍有许多悬而未决的问题有待探索。我们在这里列出了其中的一些。

1. RL 在从人类反馈中学习有多重要？我们能否通过在 IFT 或 SFT 中使用更高质量的数据进行训练来获得 RLHF 的性能？
2. 为了安全起见，Sparrow 中的 SFT+ RLHF 与 LaMDA 中仅使用 SFT 相比如何？
3. 鉴于我们有 IFT、SFT、CoT 和 RLHF，需要多少预训练？权衡是什么？人们应该使用的最佳基础模型是什么（公开的和非公开的）？
4. 本文中引用的许多模型都经过[red-teaming](https://arxiv.org/abs/2209.07858)的精心设计，工程师专门搜索故障模式并影响未来的训练（提示和方法）基于公开的问题。我们如何系统地记录这些方法的效果并重现它们？

PS：如果您发现本博客中的任何信息缺失或不正确，请告知我们。

***************引文******************

`Rajani 等人，“是什么让对话代理有用？”，Hugging Face Blog，2023。

中文提供引用：

```
@article{rajani2023ift,
  作者 = {Rajani、Nazneen 和 Lambert、Nathan 和 Sanh、Victor 和 Wolf、Thomas}，
  title = {什么使对话代理有用？},
  journal = {抱脸博客},
  年 = {2023},
  注意 = {https://huggingface.co/blog/dialog-agents},
}
```