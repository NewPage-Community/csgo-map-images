# CSGO Map Images

This repository fork from https://github.com/KZGlobalTeam/map-images.

Images for global CSGO maps available in the following:
- Full (1920x1080) - JPG/WEBP
- Medium (512x288) - JPG/WEBP
- Thumbnail (200x113) - JPG/WEBP

Images in the [source directory](./images) are used to build the variants, high-quality images are preferred.

## Usage

Generated images are in the [public](https://github.com/NewPage-Community/csgo-map-images/tree/public) branch.  
This repository is also hosted on [GitHub Pages](https://newpage-community.github.io/csgo-map-images/).

The following are available:
- `maps.json` and `maps.min.json` - A JSON file containing all the images and their urls.
- `images` - Directory where `full` JPG images are generated.
- `mediums` - Directory where `medium` JPG images are generated.
- `thumbnails` - Directory where `thumbnail` JPG images are generated.
- `webp` - Directory where `full` WEBP images are generated.
- `webp/medium` - Directory where `medium` WEBP images are generated.
- `webp/thumb` - Directory where `thumbnail` WEBP images are generated.

## Examples

#### I want to use full- sized kz_wetbricks in WEBP format
- https://github.com/NewPage-Community/csgo-map-images/raw/public/webp/kz_wetbricks.webp

#### I want to use medium- sized bkz_apricity_v3 in JPG format
- https://github.com/NewPage-Community/csgo-map-images/raw/public/mediums/bkz_apricity_v3.jpg

#### I want to retrieve all the map images and their urls as JSON
- https://github.com/NewPage-Community/csgo-map-images/raw/public/maps.json
- https://github.com/NewPage-Community/csgo-map-images/raw/public/maps.min.json

## Contributing
If you would like to add missing map images, follow the steps:
1. [Fork this repository](https://github.com/NewPage-Community/csgo-map-images/fork).
2. Upload the images to the `images` directory in your repository.
3. Commit and push your changes.
4. Create a pull request from your repository to here.

# Thanks
Most images is from Vauff.
The sync scripts make depend on thier work. [Maunz-Discord](https://github.com/Vauff/Maunz-Discord)
