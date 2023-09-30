/* <div class="item-list">
    <div class="item-list__img"><img src="../assets/img.svg" alt="img"></div>
    <div class="item-list__info">
        <div class="item-list__info-title">제목</div>
        <div class="item-list__info-meta">어딘가 10초 전</div>
        <div class="item-list__info-price">100만원</div>
    </div>
</div> */

const calcTime = (timestamp) => {
  const curTime = new Date().getTime() - 9 * 60 * 60 * 1000;
  const time = new Date(curTime - timestamp);
  const hour = time.getHours();
  const min = time.getMinutes();
  const sec = time.getSeconds();

  if (hour > 0) return `${hour} 시간 전`;
  else if (min > 0) return `${min} 분 전`;
  else if (sec > 0) return `${sec} 초 전`;
  else "방금 전";
};

const renderData = (data) => {
  const main = document.querySelector("main");
  data.reverse().forEach(async (obj) => {
    const itemListDiv = document.createElement("div");
    itemListDiv.className = "item-list";

    const imageDiv = document.createElement("div");
    imageDiv.className = "item-list__img";

    const img = document.createElement("img");
    const res = await fetch(`/images/${obj.id}`);
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    img.src = url;
    img.alt = img;

    const itemListInfoDiv = document.createElement("div");
    itemListInfoDiv.className = "item-list__info";

    const itemListInfoTitleDiv = document.createElement("div");
    itemListInfoTitleDiv.className = "item-list__info-title";
    itemListInfoTitleDiv.innerText = obj.title;

    const itemListInfoMetaDiv = document.createElement("div");
    itemListInfoMetaDiv.className = "item-list__info-meta";
    itemListInfoMetaDiv.innerText = obj.place + " " + calcTime(obj.insertAt);

    const itemListInfoPriceDiv = document.createElement("div");
    itemListInfoPriceDiv.className = "item-list__info-price";
    itemListInfoPriceDiv.innerText = obj.price;

    imageDiv.appendChild(img);
    itemListDiv.appendChild(imageDiv);
    itemListInfoDiv.appendChild(itemListInfoTitleDiv);
    itemListInfoDiv.appendChild(itemListInfoMetaDiv);
    itemListInfoDiv.appendChild(itemListInfoPriceDiv);
    itemListDiv.appendChild(itemListInfoDiv);
    main.appendChild(itemListDiv);
  });
};

const fetchList = async () => {
  const res = await fetch("/items");
  const data = await res.json();
  renderData(data);
};

fetchList();
