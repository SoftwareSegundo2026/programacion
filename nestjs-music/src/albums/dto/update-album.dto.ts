import { PartialType } from '@nestjs/mapped-types';
import { CreateAlbumDto } from './create-album.dto.js';

export class UpdateAlbumDto extends PartialType(CreateAlbumDto) {}
