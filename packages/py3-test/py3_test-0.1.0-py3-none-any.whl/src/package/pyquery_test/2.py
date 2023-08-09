"""
@Time   : 2018/12/27
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
from pyquery import PyQuery as pq

html = """
<!--star-->
<div class="desr clear">
<img class="lazy" src="http://img.zx123.cn/Resources/zx123cn/uploadfile/nwes/97a129f725efe074a001aa99d4bc6374.png" alt="槟榔家具"/>
<p class="desc">　槟榔家具是荣麟旗下的自有品牌之一。荣麟是一家集生产、研发、销售为一体的专业化家具连锁，旗下拥有槟榔、京瓷、梧桐三大家具系列。槟榔作为旗下最为知名的品牌，它的诞生是在国内的家具市场中掀起了一股东南亚之风。而在以前，东南亚风格的家具在国内是市场上是极为缺失的，槟榔家具的诞生弥补了市场的这一空缺，将家具的产品风格推向了另一种流行风尚。</p>


</div><div class="dedo"><h3>目录</h3><div class="deed">

<a href="http://www.zx123.cn/baike/1271110.html#tag1" title="槟榔家具好吗">1、槟榔家具好吗</a>
<a href="http://www.zx123.cn/baike/1271110.html#tag2" title="槟榔家具价格">2、槟榔家具价格</a>



</div></div><div class="deer"><h2 id="tag1"><span>1</span>槟榔家具好吗 </h2>


<p align="center">
<img class="lazy" src="http://img.zx123.cn/Resources/zx123cn/uploadfile/nwes/6c3ebbb0de85373cf7b8bc3357cf6dd7.jpg" width="600" height="339" title="槟榔家具好吗" alt="槟榔家具好吗"/>
</p>
<p>
       1、槟榔家具对于家具的设计是非常富有原创风格，始终坚持着要以原创的风格在家具市场中立足，这样的设计理念使得槟榔家具开创了新风尚。槟榔家具中不仅只是坚持原创，还将企业中对东西方文化的感受和理解融入到对家具的生产中。槟榔家具坚持建立品牌风格，对品牌的设计和文化与实体家具有一个良好的结合，在家具市场中独树一帜，领导家具风尚。
</p>
<p>
      2、槟榔家具的生产中，对制作家具的材料极为严格，追求精益求精采用高端品质的水曲柳木材，这样的木材能够使得家具耐用性提高。在家具的表面漆的选材中，选择较为环保的半透明漆和匠心的<a target="_blank" href="http://www.zx123.cn/baike/1271110.html"><strong><span style="color:#E53333;">刷油漆</span></strong></a>工艺，无毒无味是它的特点。槟榔家具中最大的特点就是它的结构设计，能够使家具最大程度抵抗承受能力。
</p>
<p>
      3、槟榔家具的用料材质体现了其不羁的品质，精选用整体进口的俄罗斯水曲柳，保证了家具的经久耐用，长时间使用也能保证其不变形。在漆料的选择上，采用的是国际最顶级的PU半透明漆，源自于意大利，经过了严格的质量认证，确保家具的绿色环保，无毒无味。槟榔家具最具特色的其结构，槟榔家具其内部没有一颗钉子，均采用榫卯结构，其可以最大程度的提高家具的承重能力和抗形变能力。
</p>



<h2 id="tag2"><span>2</span>槟榔家具价格 </h2>

<p align="center">
<img class="lazy" src="http://img.zx123.cn/Resources/zx123cn/uploadfile/nwes/737af418834be2693a5b3c57655f638d.jpg" width="565" height="323" title="槟榔家具价格" alt="槟榔家具价格"/>
</p>
<p>
<br/>
</p>
<p>
      槟榔W03六斗柜                            价格：  10706元  。
</p>
<p>
      槟榔C01水曲柳木皮贴面梳妆台        价格：5890元。
</p>
<p>
      槟榔K11-1水曲柳木皮贴面活动架     价格：1350元。
</p>
<p>
      槟榔B03水曲柳木皮贴面床头柜        价格：2000元。
</p>
<p>
      槟榔A03L水曲柳木皮贴面双人床      价格：8860元。
</p>



</div><!--end-->
<div style="clear: both;"/>
"""

doc = pq(html)

doc(".desr").remove()
doc(".dedo").remove()
print(doc.html())
