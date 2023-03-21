import * as gm from "gm";
import * as fs from "fs";
import * as path from "path";
import * as core from "@actions/core";

import { ensureDir } from "./utils";
import { ImageFormat, ImageVariant, ImageDimensions } from "./types";

const variants: Record<ImageVariant, ImageDimensions> = {
  full: [1920, 1080],
  medium: [512, undefined],
  thumbnail: [200, undefined],
};

const variantDirs: Record<ImageFormat, Record<ImageVariant, string>> = {
  jpg: {
    full: "images",
    medium: "mediums",
    thumbnail: "thumbnails"
  },
  webp: {
    full: "webp",
    medium: "webp/medium",
    thumbnail: "webp/thumb"
  },
};

export class ImageService {
  private readonly buildDir: string;

  constructor(buildDir: string) {
    this.buildDir = buildDir;
  }

  resizeImage(image: string, destPath: string, [w, h]: ImageDimensions) {
    return new Promise((resolve) => {
      try {
        gm(image)
          .resize(w, h, "!")
          .noProfile()
          .write(destPath, (err) => {
            if (!err) return;
            core.warning(`Write failed ${image} to ${destPath} (${w}x${h})`);
            core.warning(err);
          });
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      } catch (err: any) {
        core.warning(`Resize failed ${image} to ${destPath} (${w}x${h})`);
        core.warning(err);
      }
      resolve(destPath);
    });
  }

  removeImage(srcImage: string) {
    return Promise.all([
      this.removeImageFormat(srcImage, ImageFormat.JPG),
      this.removeImageFormat(srcImage, ImageFormat.WEBP),
    ]);
  }

  removeImageFormat(srcImage: string, format: ImageFormat) {
    return Promise.all([
      this.removeImageVariant(srcImage, format, ImageVariant.Full),
      this.removeImageVariant(srcImage, format, ImageVariant.Medium),
      this.removeImageVariant(srcImage, format, ImageVariant.Thumbnail),
    ]);
  }

  removeImageVariant(srcImage: string, format: ImageFormat, variant: ImageVariant) {
    const destDir = path.join(this.buildDir, variantDirs[format][variant]);

    const imageName = path.parse(srcImage).name;
    const destImage = path.join(destDir, `${imageName}.${format}`);

    return fs.promises.rm(destImage, { force: true });
  }

  generateImage(srcImage: string) {
    return Promise.all([
      this.generateImageFormat(srcImage, ImageFormat.JPG),
      this.generateImageFormat(srcImage, ImageFormat.WEBP),
    ]);
  }

  generateImageFormat(srcImage: string, format: ImageFormat) {
    return Promise.all([
      this.generateImageVariant(srcImage, format, ImageVariant.Full),
      this.generateImageVariant(srcImage, format, ImageVariant.Medium),
      this.generateImageVariant(srcImage, format, ImageVariant.Thumbnail),
    ]);
  }

  async generateImageVariant(srcImage: string, format: ImageFormat, variant: ImageVariant) {
    const destDir = path.join(this.buildDir, variantDirs[format][variant]);

    await ensureDir(destDir);

    const imageName = path.parse(srcImage).name;
    const destImage = path.join(destDir, `${imageName}.${format}`);

    const dimensions = variants[variant];

    return this.resizeImage(srcImage, destImage, dimensions);
  }
}
