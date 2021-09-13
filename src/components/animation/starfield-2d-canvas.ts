/* eslint max-classes-per-file: ["error", 10] */

const { requestAnimationFrame, cancelAnimationFrame } = window;

const randomForMinMax = (min: number, max: number) => {
  return min + (Math.random() * (max - min));
};

const randomXYZ = (width: number, height: number, depth: number) => {
  const x = randomForMinMax(-width, width);
  const y = randomForMinMax(-height, height);
  const z = randomForMinMax(1, depth);
  return { x, y, z };
};

class Point {
  x: number;

  y: number;

  z: number;

  constructor(x: number, y: number, z: number) {
    this.x = x;
    this.y = y;
    this.z = z;
  }

  setZ(z: number) {
    this.z = z;
  }

  setXYZ(x: number, y: number, z: number) {
    this.x = x;
    this.y = y;
    this.z = z;
  }
}

class Starfield {
  ctx: CanvasRenderingContext2D|null;

  animationId: number = -1;

  width: number;

  height: number;

  x: number = 0;

  y: number = 0;

  originX: number = 0;

  originY: number = 0;

  depth: number = 1000;

  maxPointSize: number = 8;

  points: Array<Point> = [];

  lastRenderTime: number = 0;

  constructor(canvas: HTMLCanvasElement) {
    const ctx = canvas.getContext('2d');
    // @ts-ignore
    window.ctx = ctx;
    if (ctx) {
      ctx.fillStyle = 'rgb(0,0,0)';
      ctx.shadowColor = 'rgb(255,255,255)';
      ctx.globalAlpha = 0.9;
    }
    this.width = canvas.width;
    this.height = canvas.height;
    this.ctx = ctx;
    this.start();
  }

  start = () => {
    this.initializeOrigin();
    this.initializePoints(200);
    this.run(0);
  }

  stop = () => {
    cancelAnimationFrame(this.animationId);
  }

  resume = () => {
    this.run(0);
  }

  run = (time: number) => {
    this.render(time).then(() => {});
    this.animationId = requestAnimationFrame(this.run);
  }

  initializeOrigin = () => {
    this.originX = Math.round(this.width / 2);
    this.originY = Math.round(this.height / 2);
  }

  initializePoints = (numPoints: number = 0) => {
    const points = [];
    for (let i = 0; i < numPoints; i += 1) {
      const { x, y, z } = randomXYZ(this.width, this.height, this.depth);
      const point = new Point(x, y, z);
      points.push(point);
    }
    this.points = points;
    console.table(this.points);
  }

  updatePoints = async (step: number) => {
    for (let i = 0; i < this.points.length; i += 1) {
      const point = this.points[i];
      if (point.z > 2) {
        // point.z -= step;
        point.setZ(point.z - step);
      } else {
        const { x, y, z } = randomXYZ(this.width, this.height, this.depth);
        point.setXYZ(x, y, z);
      }
    }
  }

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  drawPoint = (point: Point) => {
    const k = 256 / point.z;
    const x = point.x * k + this.originX;
    const y = point.y * k + this.originY;
    // const size = 10;
    const size = ((this.depth - point.z) / this.depth) * this.maxPointSize;
    if (this.ctx) {
      this.ctx.beginPath();
      this.ctx.ellipse(x, y, size, size, 0, 0, 10);
      this.ctx.fill();
    }
  }

  async render(time: number) {
    const timeDelta = (time - this.lastRenderTime);
    this.lastRenderTime = time;
    const step = timeDelta * 0.05;
    await this.updatePoints(step);
    // console.debug(this.points[0]);
    // console.table(this.points);
    // console.debug('Starfield - render loop', this.x, this.y);
    if (this.ctx) {
      this.ctx.clearRect(0, 0, this.width, this.height);
    }
    for (let i = 0; i < this.points.length; i += 1) {
      this.drawPoint(this.points[i]);
    }
  }
}

export { Starfield };
