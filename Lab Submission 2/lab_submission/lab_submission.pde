ArrayList<PImage> texturePool;
ArrayList<Ball> balls;
java.util.Random rand;

void setup() {
  size(1000,600,P3D);
  texturePool = new ArrayList<PImage>();
  texturePool.add(loadImage("earth.jpg"));
  texturePool.add(loadImage("moon.jpg"));
  texturePool.add(loadImage("kevin.png"));
  balls = new ArrayList<Ball>();
  rand = new java.util.Random();
}

void draw() {
  background(0);
  for (Ball b : balls) {
    b.draw();
  }
  
}

void mousePressed() {
  balls.add(new Ball(new javafx.geometry.Point3D(mouseX, mouseY, 0)));
}

class Ball {
  
  javafx.geometry.Point3D point;
  javafx.geometry.Point3D velocity;
  final int RADIUS = 30;
  PShape sphere;
  
  Ball(javafx.geometry.Point3D point) {
    this.point = point;
    velocity = new javafx.geometry.Point3D(4,5,-5);
    sphere = createShape(SPHERE, 30);
    sphere.setStroke(false);
    sphere.setTexture(texturePool.get(rand.nextInt(texturePool.size())));
  }
  
  void draw() {
    pushMatrix();
    translate((int)point.getX(), (int)point.getY(), (int)point.getZ());
    shape(sphere);
    point = point.add(velocity);
    
    if (point.getX() + RADIUS >= width) {
        if (velocity.getX() >= 0) {
          javafx.geometry.Point3D subtraction = new javafx.geometry.Point3D(2*velocity.getX(), 0,0);
          velocity = velocity.subtract(subtraction);
        }
    } else if (point.getX() - RADIUS <= 0) {
        if (velocity.getX() <= 0){
          javafx.geometry.Point3D addittion = new javafx.geometry.Point3D(-2*velocity.getX(), 0,0);
          velocity = velocity.add(addittion);
        }
    }
    
    if (point.getY() + RADIUS >= height) {
        if (velocity.getY() >= 0) {
          javafx.geometry.Point3D subtraction = new javafx.geometry.Point3D(0, 2*velocity.getY(),0);
          velocity = velocity.subtract(subtraction);
        }
    } else if (point.getY() - RADIUS <= 0) {
        if (velocity.getY() <= 0){
          javafx.geometry.Point3D addittion = new javafx.geometry.Point3D(0, -2*velocity.getY(),0);
          velocity = velocity.add(addittion);
        }
    }
    
    if (point.getZ() <= -300) {
      if (velocity.getZ() <= 0) {
        javafx.geometry.Point3D addittion = new javafx.geometry.Point3D(0,0,-2*velocity.getZ());
        velocity = velocity.add(addittion);
      }
    } else if (point.getZ() >= 100) {
      if (velocity.getZ() >= 0) {
        javafx.geometry.Point3D subtraction = new javafx.geometry.Point3D(0,0,2*velocity.getZ());
        velocity = velocity.subtract(subtraction);
      }
    }
    popMatrix();
  }
  
  void collide(Ball other) {
    if (this == other)
      return;
    if (point.distance(other.point) < 30) {
      //resolve colission
    }
  }

}
