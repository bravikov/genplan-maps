let workspaceContainer = document.createElement("div");
workspaceContainer.id = "workspace";

let pretilesContainer = document.createElement("div");
pretilesContainer.id = "pretiles";
workspaceContainer.appendChild(pretilesContainer);

let tilesContainer = document.createElement("div");
tilesContainer.id = "tiles";
pretilesContainer.appendChild(tilesContainer);

function main() {

// Включает и отключает отладочный вывод.
const isDebug = true;

if (isDebug) {
    var debug = console.log.bind(window.console)
}
else {
    var debug = function(){}
}

// Размер тайла. Тайл квадратный: 256 x 256 пикселей.
const tileSize = 256;

const tilesLevelCount = tilesConfig.levels.length;

let tilesLevel = Math.floor(tilesLevelCount / 2);

class Point {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }
}

class Size {
    constructor(width, height) {
        this.width = width;
        this.height = height;
    }
}

function getTilesCenter() {
    const level = tilesConfig.levels[tilesLevel]
    const width = (level.tileCount.x - 1) * tileSize + level.lastTileSize.width;
    const height = (level.tileCount.y - 1) * tileSize + level.lastTileSize.height;
    return new Point(width / 2, height / 2);
}

function getWorkspaceSize() {
    return new Size(workspaceContainer.offsetWidth, workspaceContainer.offsetHeight);
}

/* Координаты начального тайла.
    * Начальный тайл рисуется в левом верхнем углу тайлового контейнера.
    * Начальная позиция расчитывается так, чтобы центр изображения был в центре видимой области.
    * Координаты меняются при перемещении тайлового контейнера. */

    let startTilePosition = new Point(0, 0);

function setStartTilePosition(position) {
    startTilePosition = position;
    debug("Start tile position:", startTilePosition.x, startTilePosition.y)
}

function setStartTilePositionByXY(x, y) {
    setStartTilePosition(new Point(x, y));
}

// Координаты тайлового контейнера. Меняются при перемещении контейнера.
let tilesContainerX = 0;
let tilesContainerY = 0;

// Координаты фокуса.
// Фокус — точка, относительно которой происходит масштабирование.
// Для мышки, фокус — это позиция курсора.
// Для тачпада, фокус — это центральная позиция между пальцами.
let focusPosition = new Point(0, 0)

function setFocusPosition(x , y) {
    focusPosition = new Point(x, y);
    debug("Focus position:", focusPosition.x, focusPosition.y)
}

function placeElement(element, xPos, yPos) {
    element.style.transform = "translate3d(" + xPos + "px, " + yPos + "px, 0)";
}

function moveTiles(xPos, yPos) {
    placeElement(tilesContainer, xPos, yPos);
}

function setDefaultStartTilePosition() {
    const tilesCenter = getTilesCenter();
    const workspaceSize = getWorkspaceSize();
    const precisionStartTilePosition = new Point(
        Math.floor(tilesCenter.x - (workspaceSize.width / 2)),
        Math.floor(tilesCenter.y - (workspaceSize.height / 2)),
    );

    tilesContainerX = -(precisionStartTilePosition.x % tileSize);
    tilesContainerY = -(precisionStartTilePosition.y % tileSize);

    setFocusPosition(tilesCenter.x, tilesCenter.y);

    setStartTilePosition(precisionStartTilePosition);
    moveTiles(tilesContainerX, tilesContainerY);
}

setDefaultStartTilePosition();

const invalidTileNumber = -1;

function tileNumber(tilesCountX, tileX, tileY) {
    return tilesCountX * tileY + tileX;
}

class Tile {
    constructor(element) {
        this.element = element;
    }
}

let tilesMap = new Map();

function loadTiles() {
    // Количество тайлов по горизонтали.
    const tilesCountX = tilesConfig.levels[tilesLevel].tileCount.x;
    // Количество тайлов по вертикали.
    const tilesCountY = tilesConfig.levels[tilesLevel].tileCount.y;

    let startTileX = Math.floor(startTilePosition.x / tileSize);
    let startTileY = Math.floor(startTilePosition.y / tileSize);
    
    const workspaceWidth = workspaceContainer.offsetWidth;
    const workspaceHeight = workspaceContainer.offsetHeight;
    
    // На один тайл больше, чтобы при перемещении карты вправо не было пустого места слева.
    workspaceTilesCountX = Math.ceil(workspaceWidth / tileSize) + 1;
    workspaceTilesCountY = Math.ceil(workspaceHeight / tileSize) + 1;

    let tiles = []

    for (let y = 0; y < workspaceTilesCountY; y++) {
        let xTiles = []
        const tileY = startTileY + y;
        if (tileY >= tilesCountY) {
            break;
        }
        for (let x = 0; x < workspaceTilesCountX; x++) {
            const tileX = startTileX + x;
            if (tileX >= tilesCountX) {
                break;
            }
            let n = invalidTileNumber;
            if (tileX >= 0 && tileY >= 0) {
                n = tileNumber(tilesCountX, tileX, tileY);
            }
            xTiles.push(n);
        }
        tiles.push(xTiles);
    }

    let visibleTilesNumbers = new Set();

    // Отрисовка тайлов.
    for (let y = 0; y < tiles.length; y++) {
        for (let x = 0; x < tiles[y].length; x++) {
            let tileImg = document.createElement("img");
            tileImg.className = "tile";
            const tileNumber = tiles[y][x];
            if (tileNumber === invalidTileNumber) {
                continue;
            }
            visibleTilesNumbers.add(tileNumber);
            if (tilesMap.has(tileNumber)) {
                continue;
            }
            tileImg.src = mapPath + "/tiles/" + tilesLevel + "/tile-" + tileNumber + ".png";

            let offsetX = 0;
            let offsetY = 0;
            if (tilesContainerX !== 0) {
                offsetX = tileSize * (Math.floor(tilesContainerX / tileSize) + 1);
            }
            if (tilesContainerY !== 0) {
                offsetY = tileSize * (Math.floor(tilesContainerY / tileSize) + 1);
            }

            const elementPositionX = x * tileSize - offsetX;
            const elementPositionY = y * tileSize - offsetY;
            placeElement(tileImg, elementPositionX, elementPositionY);
            tilesContainer.appendChild(tileImg);
            let tile = new Tile(tileImg);
            tilesMap.set(tileNumber, tile);
        }
    }

    // Удаление тайлов, которых не видно.
    tilesMap.forEach((value, key, map) => {
        if (visibleTilesNumbers.has(key)) {
            return;
        }
        else {
            value.element.remove();
            map.delete(key);
        }
    });
}

moveTiles(tilesContainerX, tilesContainerY);
loadTiles();

// Предотвращает перехват инициативы браузером при перемещении карты.
workspaceContainer.ondragstart = function() {
    return false;
};

let primaryPointerId = NaN;
let secondaryPointerId = NaN;
let pointerCount = 0;

class Pointer {
    constructor(position) {
        this.position = position;
    }
}

// Словарь содержит все указывающие объекты экрана, активные в данный момент.
// Ключ: pointer ID, значение: Pointer
let activePointersMap = new Map();

function debugPointers() {
    debug("Pointers: [")
    activePointersMap.forEach((value, key, map) => {
        debug(`  Pointer ${key} [${value.x}, ${value.y}]`)
    });
    debug("]")
}

function addPointers(event) {
    const pointerId = event.pointerId;
    debug(`Pointer ${pointerId}`)
    activePointersMap.set(event.pointerId, new Point(event.offsetX, event.offsetY))
    debugPointers();
}

function delPointers(event) {
    const pointerId = event.pointerId;
    debug(`Pointer ${pointerId}`)
    if (activePointersMap.has(pointerId)) {
        activePointersMap.delete(pointerId);
    }
    debugPointers();
}

workspaceContainer.addEventListener('pointerdown', event => {
    debug("pointerdown");
    event.preventDefault();
    workspaceContainer.style.cursor = "grabbing";
    addPointers(event);
});

workspaceContainer.addEventListener('pointerup', event => {
    debug("pointerup");
    event.preventDefault();
    workspaceContainer.style.cursor = "default";
    loadTiles();
    delPointers(event);
});

workspaceContainer.addEventListener('pointercancel', event => {
    debug("pointercancel");
    event.preventDefault();
    delPointers(event);
});

function zoom(zoomIn) {
    let scale = 0;
    if (zoomIn) {
        debug("Zoom in.");
        if (tilesLevel > 0) {
            tilesLevel -= 1;
            scale = 2;
        }
        else {
            return;
        }
    }
    else {
        debug("Zoom out.");
        if (tilesLevel < tilesLevelCount - 1) {
            tilesLevel += 1;
            scale = 0.5;
        }
        else {
            return;
        }
    }
    const workspaceSize = getWorkspaceSize();

    const center = new Point(
        Math.floor((startTilePosition.x + focusPosition.x) * scale),
        Math.floor((startTilePosition.y + focusPosition.y) * scale)
    );

    // Удаление всех тайлов.
    tilesMap.forEach((value, key, map) => {
        value.element.remove();
        map.delete(key);
    });

    let precisionStartTilePosition = center;
    precisionStartTilePosition.x -= focusPosition.x;
    precisionStartTilePosition.y -= focusPosition.y;

    tilesContainerX = -(precisionStartTilePosition.x % tileSize);
    tilesContainerY = -(precisionStartTilePosition.y % tileSize);

    setStartTilePosition(precisionStartTilePosition);
    moveTiles(tilesContainerX, tilesContainerY);
    loadTiles();
}

// Количество пикселей, на которые изменился масштабирующий прямоугольник.
// Изменяется при масштабировании с помощью пальцев.
let pointersScale_px = 0;

// Порог при котором изменяется уровень тайлов и сбрасывается pointersScale_px.
const pointersScaleThreshold_px = 15;

workspaceContainer.addEventListener('pointermove', event => {
    debug("pointermove");
    event.preventDefault();
    const pointerId = event.pointerId;
    debug(`Pointer ${pointerId}`)

    if (activePointersMap.size < 2) {
        setFocusPosition(event.offsetX, event.offsetY)
    }

    if (activePointersMap.size > 2) {
        // Ничего не делаем, если на экране много указателей.
        return;
    }

    if (activePointersMap.size < 2) {
        pointersScale_px = 0;
    }

    if (!activePointersMap.has(pointerId)) {
        return;
    }

    let currentPointer = activePointersMap.get(pointerId);

    debug("Current pointer position: ", currentPointer.x, currentPointer.y)

    const pointerDeltaX = event.offsetX - currentPointer.x;
    const pointerDeltaY = event.offsetY - currentPointer.y;

    // Один указатель на экране. Мышь или палец.
    // Двигаем карту.
    if (activePointersMap.size === 1) {
        debug("Перемещение тайлов.");

        const newTilesContainerX = tilesContainerX + pointerDeltaX;
        const newTilesContainerY = tilesContainerY + pointerDeltaY;

        setStartTilePositionByXY(
            startTilePosition.x + tilesContainerX - newTilesContainerX,
            startTilePosition.y + tilesContainerY - newTilesContainerY
        );

        tilesContainerX = newTilesContainerX;
        tilesContainerY = newTilesContainerY;

        moveTiles(newTilesContainerX, newTilesContainerY);
    }

    // Два указателя на экране. Два пальца.
    // Масштабиуем.
    if (activePointersMap.size === 2 && event.isPrimary) {
        debug("Масштабирование пальцами.");
        pointersScale_px -= pointerDeltaY;
        debug("pointersScale_px:", pointersScale_px);
        debug("pointerDeltaY:", pointerDeltaY);

        if (Math.abs(pointersScale_px) >= pointersScaleThreshold_px) {
            const zoomIn = Math.sign(pointersScale_px) == 1;
            if (zoomIn) {
                console.log("Zoom In");
            }
            else {
                console.log("Zoom Out");
            }
            zoom(zoomIn);
            pointersScale_px = 0;
        }
    }

    currentPointer.x = event.offsetX;
    currentPointer.y = event.offsetY;
});

let wheel_is_slepping = false;

workspaceContainer.addEventListener("wheel", event => {
    debug("wheel");
    debug(event.deltaX, event.deltaY, event.deltaZ, event.deltaMode, event.wheelDelta, event.wheelDeltaX, event.wheelDeltaY);
    if (wheel_is_slepping) {
        return;
    }

    wheel_is_slepping = true;
    setTimeout(function wakeup_wheel() {
        wheel_is_slepping = false;
    }, 200);

    event.preventDefault();
    const zoomIn = Math.sign(event.deltaY) == -1;
    zoom(zoomIn);
});

} // function main()

window.onload = function() {
    document.getElementsByTagName("body")[0].appendChild(workspaceContainer);
    document.title = mapTitle;
    main();
};
