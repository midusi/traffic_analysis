<template>
  <div>
    <div class="container">
      <video ref="video" src="./otro minuto.mp4" @loadeddata="adjustCanvasSize"></video>
      <canvas ref="canvas"></canvas>
    </div>

    <div class="buttons">
      <button @click="finalizarPoly">Finalizar Polígono</button>
      <button @click="cancelarPoly">Cancelar Polígono</button>
      <button @click="deshacerPoly">Deshacer Polígono</button>
      <button @click="rehacerPoly">Rehacer Polígono</button>
      <button @click="limpiarCanvas">Limpiar Canvas</button>
    </div>
    
    <label for="tipo">Tipo</label>
    <select v-model="tipo">
      <option value="Entrada">Entrada</option>
      <option value="Salida">Salida</option>
      <option value="Exclusion">Exclusión</option>
    </select>

    <ol ref="polygonList">
      <li v-for="(polygon, index) in polygons" :key="index">
        {{ polygon.tipo }}
        <button @click="eliminarPoly(index)">Eliminar</button>
        <button @click="cambiarTipo(index)">Cambiar Tipo</button>
      </li>
    </ol>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isDrawing: false,
      tipo: 'Entrada',
      currentPolygon: { points: [], tipo: 'Entrada' },
      polygons: [],
      deletedPolygons: [],
      highlightedPolygonIndex: null,
      canvas: null,
      ctx: null,
      polygonList: null,
      colores: {
        Entrada: 'lightgreen',
        Salida: 'blue',
        Exclusion: 'red'
      }
    };
  },
  methods: {
    adjustCanvasSize() {
      const canvas = this.$refs.canvas;
      const video = this.$refs.video;
      canvas.width = video.clientWidth;
      canvas.height = video.clientHeight;
    },
    getMousePosition(event) {
      const canvas = this.$refs.canvas;
      const rect = canvas.getBoundingClientRect();
      return [event.clientX - rect.left, event.clientY - rect.top];
    },
    drawPolygons(polys) {
      const ctx = this.ctx;
      ctx.clearRect(0, 0, this.canvas.width, this.canvas.height); // Limpiar canvas
      polys.forEach((polygon, index) => {
        ctx.beginPath();
        ctx.moveTo(polygon.points[0][0], polygon.points[0][1]);
        for (let i = 1; i < polygon.points.length; i++) {
          ctx.lineTo(polygon.points[i][0], polygon.points[i][1]);
        }
        ctx.closePath();
        ctx.strokeStyle = this.colores[polygon.tipo];
        ctx.lineWidth = index === this.highlightedPolygonIndex ? 2.5 : 1.5; // Aumenta el grosor si está resaltado
        ctx.stroke();
      });
    },
    cleanActualPath() {
      this.currentPolygon.points = [];
      this.isDrawing = false;
      this.drawPolygons(this.polygons);
    },
    deshacerPoly() {
      if (this.polygons.length > 0) {
        this.deletedPolygons.push(this.polygons.pop());
        this.cleanActualPath();
      }
    },
    rehacerPoly() {
      if (this.deletedPolygons.length > 0) {
        this.polygons.push(this.deletedPolygons.pop());
        this.cleanActualPath();
      }
    },
    finalizarPoly() {
      if (this.currentPolygon.points.length >= 3) {
        this.polygons.push({ points: [...this.currentPolygon.points], tipo: this.tipo });
      }
      this.cleanActualPath();
    },
    cancelarPoly() {
      this.cleanActualPath();
    },
    limpiarCanvas() {
      if (confirm("¿Estás seguro?")) {
        this.polygons = [];
        this.deletedPolygons = [];
        this.cleanActualPath();
      }
    },
    eliminarPoly(index) {
      this.polygons.splice(index, 1);
      this.cleanActualPath();
    },
    cambiarTipo(index) {
      const polygon = this.polygons[index];
      polygon.tipo = this.ciclarTipo(polygon.tipo);
      this.cleanActualPath();
    },
    toggleTipo() {
      this.tipo = this.ciclarTipo(this.tipo);
    },
    ciclarTipo(tipo) {
      const tipos = ['Entrada', 'Salida', 'Exclusion'];
      let i = tipos.indexOf(tipo);
      i = (i + 1) % tipos.length;
      return tipos[i];
    },
    highlightPolygon(index) {
      if (this.highlightedPolygonIndex !== index) {
        this.removePolygonHighlight();

        const listItem = this.polygonList.children[index];
        listItem.style.color = 'yellow';

        this.highlightedPolygonIndex = index;
        this.cleanActualPath();
      }
    },
    removePolygonHighlight() {
      if (this.highlightedPolygonIndex !== null) {
        const previousListItem = this.polygonList.children[this.highlightedPolygonIndex]
        if (previousListItem) previousListItem.style.color = '';

        this.highlightedPolygonIndex = null;
        this.cleanActualPath(); // Redibuja para quitar el resaltado
      }
    },
    isMouseInPolygon(mousePos, polygon) {
      let isInside = false;
      for (let i = 0, j = polygon.points.length - 1; i < polygon.points.length; j = i++) {
        const xi = polygon.points[i][0], yi = polygon.points[i][1];
        const xj = polygon.points[j][0], yj = polygon.points[j][1];
        const mousePosX = mousePos[0];
        const mousePosY = mousePos[1];
        
        const intersect = ((yi > mousePosY) !== (yj > mousePosY)) &&
                          (mousePosX < (xj - xi) * (mousePosY - yi) / (yj - yi) + xi);
        if (intersect) isInside = !isInside;
      }
      return isInside;
    },
  },
  mounted() {
    this.polygonList = this.$refs.polygonList
    this.canvas = this.$refs.canvas;
    this.ctx = this.canvas.getContext('2d');

    this.canvas.addEventListener('mousedown', (event) => {
      this.isDrawing = true;
      const pos = this.getMousePosition(event);
      this.currentPolygon.points.push(pos);
    });

    this.canvas.addEventListener('mousemove', (event) => {
      const pos = this.getMousePosition(event);
      if(this.isDrawing) {
        const tempPolygon = { points: [...this.currentPolygon.points, pos], tipo: this.currentPolygon.tipo };
        this.drawPolygons([...this.polygons, tempPolygon]);
      } else {
        let polygonFound = false;

        this.polygons.forEach((polygon, index) => {
          if (this.isMouseInPolygon(pos, polygon)) {
            this.highlightPolygon(index);
            polygonFound = true;
          }
        });

        if (!polygonFound && this.highlightedPolygonIndex !== null) {
          this.removePolygonHighlight();
        }
      }
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'f') this.finalizarPoly();
      else if (e.ctrlKey && e.key === 'z') this.deshacerPoly();
      else if (e.ctrlKey && e.key === 'r') {
        e.preventDefault();
        e.stopPropagation();
        this.rehacerPoly();
      }
      else if (e.key === 'Escape') this.cancelarPoly();
      else if (e.key === 't') this.toggleTipo();
    });
  },
  watch: {
    tipo() {
      this.currentPolygon.tipo = this.tipo;
    }
  }
};
</script>

<style scoped>
body {
  margin: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #333;
}
.container {
  position: relative;
}
video {
  width: 640px;
  height: 360px;
}
canvas {
  position: absolute;
  top: 0;
  left: 0;
}
.buttons {
  margin-top: 10px;
}
button {
  margin: 0 5px;
  padding: 5px 10px;
  font-size: 16px;
  cursor: pointer;
}
</style>

<style scoped>
.video-fluid {
  width: 100%;
  height: auto;
}
.list-group-item {
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  margin-bottom: 0.5rem;
  border-radius: 5px;
}
</style>
